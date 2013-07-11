# Casemapper
# https://github.com/sidsrivastava/Casemapper/
#
# Copyright (C) 2013 Sid Srivastava 
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from utilities import *
from OrderedDict import OrderedDict
import Config

class KeymapGroup:
  def __init__(self, name):
    self.name = name
    self.subgroups = OrderedDict()

  def getAllKeys(self):
    allKeys = []
    for keys in self.subgroups.itervalues():
      for key in keys:
        allKeys.append(key)
    return allKeys

class Keymap:
  def __init__(self):
    self.path = ""
    self.groups = []

  def load(self, path):
    # open files
    self.path = path
    data = open(self.path).readlines()
    data = removeEmptyLines(data)

    # read data
    i = 0
    while i < len(data):
      groupName = data[i].replace('#', '').strip()
      group = KeymapGroup(groupName)
      i = i + 1
      while (i < len(data)) and (data[i].find('######') == -1):
        subgroupName = data[i].split(':')[0].strip()
        subgroupKeys = data[i].split(':')[1].strip().split(',')
        subgroupKeys = [element.strip() for element in subgroupKeys]
        group.subgroups[subgroupName] = subgroupKeys
        i = i + 1
      self.groups.append(group)

    print 'Loaded keymap from "' + self.path + '".'

  def getKeys(self):
    allKeys = []
    for group in self.groups:
      for keys in group.subgroups.itervalues():
        for key in keys:
          allKeys.append(key)
    return allKeys

  def display(self):
    for group in self.groups:
      print group.name
      for label,keys in group.subgroups.iteritems():
        print "  " + label
        for key in keys:
          print "    " + key

  #### dump excel ####

  def dumpExcelData(self, excelDir, caselist):
    self.dumpExcelDataFeatures(excelDir + '/features.txt', caselist)

  def dumpExcelDataFeatures(self, excelDataPath, caselist):
    excelDataFile = open(excelDataPath, 'w')
    allKeys = caselist.getAllKeys()

    # get unique values for "protein change"
    proteinChangeUniqueValues = caselist.getUniqueValuesByKey("protein change")

    # write header
    excelDataFile.write("Feature" + "\t")
    for a in proteinChangeUniqueValues:
      excelDataFile.write(a + "\t")
    excelDataFile.write("\n\n")

    for group in self.groups:
     if group.name not in Config.ignorableGroups:
        excelDataFile.write('******** ' + group.name + ' ********\n')
        for label, keys in group.subgroups.iteritems():
          excelDataFile.write('**** ' + label + ' ****\n') 
          for key in keys:
            if (key in allKeys) and (key not in Config.nonnumericKeys):
              excelDataFile.write(key + "\t")
              for proteinChange in proteinChangeUniqueValues:
                cases = caselist.getCasesByKeyValueSecondKey("protein change", proteinChange, key)
                totalNumberCases = len(cases)
                positiveNumberCases = 0
                for case in cases:
                  if case.data[key] == "1":
                    positiveNumberCases = positiveNumberCases + 1

                excelDataFile.write(str(positiveNumberCases) + '/' + str(totalNumberCases))
                excelDataFile.write('\t')
              excelDataFile.write('\n')
          excelDataFile.write('\n')


    excelDataFile.close()
    print 'Dumped stata commands (sum) to "' +  excelDataPath + '"'
	
  #### dump stata ####

  def dumpStataCommands(self, stataDir, caselist):
    self.dumpStataCommandsListAllFeatures(stataDir + '/features_all.txt', caselist)
    self.dumpStataCommandsListsFeaturesByGroup(stataDir + '/features_groups.txt', caselist)
    self.dumpStataCommandsTabstatFeatures(stataDir + '/features_tabstat.txt', caselist)

  def dumpStataCommandsListAllFeatures(self, stataCommandsPath, caselist):
    keyCount = 0
    allKeys = caselist.getAllKeys()
    stataCommandsFile = open(stataCommandsPath, 'w')

    stataCommandsFile.write('local all_features ')
    for group in self.groups:
      if group.name not in Config.ignorableGroups:
        for key in group.getAllKeys():
          if (key in allKeys) and (key not in Config.nonnumericKeys):
            stataCommandsFile.write(stataizeVariable(key) + ' ')
            keyCount = keyCount + 1

    stataCommandsFile.close()
    print 'Dumped stata commands (list of all features) to "' + stataCommandsPath + '"'

  def dumpStataCommandsListsFeaturesByGroup(self, stataCommandsPath, caselist):
    stataCommandsFile = open(stataCommandsPath, 'w')
    allKeys = caselist.getAllKeys()

    for group in self.groups:
     if group.name not in Config.ignorableGroups:
        stataCommandsFile.write('**** ' + group.name + ' ****\n')
        for label, keys in group.subgroups.iteritems():
          stataCommandsFile.write('local ' + stataizeVariable(label) + ' ')
          for key in keys:
            if (key in allKeys) and (key not in Config.nonnumericKeys):
              stataCommandsFile.write(stataizeVariable(key) + ' ')
          stataCommandsFile.write('\n')
        stataCommandsFile.write('\n')

    stataCommandsFile.close()
    print 'Dumped stata commands (lists features by group) to "' +  stataCommandsPath + '"'

  def dumpStataCommandsTabstatFeatures(self, stataCommandsPath, caselist):
    stataCommandsFile = open(stataCommandsPath, 'w')
    allKeys = caselist.getAllKeys()

    # features by group
    for group in self.groups:
      if group.name not in Config.ignorableGroups:
        stataCommandsFile.write('**** ' + group.name + ' ****\n')
        stataCommandsFile.write('tabstat ')
        print 'Sorting keys in "' + group.name + '"...'
        groupKeys = caselist.getKeysSortedByMeans(group.getAllKeys())
        for key in groupKeys:
          if (key in allKeys) and (key not in Config.nonnumericKeys):
            stataCommandsFile.write(stataizeVariable(key) + ' ')
        stataCommandsFile.write('\n\n')


    # features by group and subroup
#    for group in self.groups:
#     if group.name not in Config.ignorableGroups:
#        stataCommandsFile.write('**** ' + group.name + ' ****\n')
#        for label, keys in group.subgroups.iteritems():
#          stataCommandsFile.write('tabstat ')
#          print 'Sorting keys in "' + label + '"...'
#          subgroupKeys = caselist.getKeysSortedByMeans(keys)
#          for key in subgroupKeys:
#            if (key in allKeys) and (key not in Config.nonnumericKeys):
#              stataCommandsFile.write(stataizeVariable(key) + ' ')
#          stataCommandsFile.write('\n')'''

    stataCommandsFile.close()
    print 'Dumped stata groups commands (tabstat) to "' +  stataCommandsPath + '"'

#  def dumpStataCommandsTabFeatures(self, stataCommandsPath, caselist):
#    stataCommandsFile = open(stataCommandsPath, 'w')
#    allKeys = caselist.getAllKeys()
#
#    for group in self.groups:
#     if group.name not in Config.ignorableGroups:
#        stataCommandsFile.write('******** ' + group.name + ' ********\n')
#        for label, keys in group.subgroups.iteritems():
#          stataCommandsFile.write('**** ' + label + ' ****\n') 
#		  # stataCommandsFile.write('local ' + stataizeVariable(label) + ' ')
#          for key in keys:
#            if (key in allKeys) and (key not in Config.nonnumericKeys):
#              stataCommandsFile.write('bysort protein_change: tab ' + stataizeVariable(key) + ' if ' + stataizeVariable(key) + ' != -1' + '\n')
#          stataCommandsFile.write('\n\n')
#        stataCommandsFile.write('\n')
#
#    stataCommandsFile.close()
#    print 'Dumped stata commands (sum) to "' +  stataCommandsPath + '"'