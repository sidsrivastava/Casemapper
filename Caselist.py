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

from copy import deepcopy
import os
import logging
from operator import itemgetter

from Case import Case
from utilities import *

# log
log = logging.getLogger('process')

class Caselist:

  def __init__(self):
    self.cases = []

  def loadCases(self, cases):
    for case in cases:
      self.cases.append(case)
    log.info('Loaded ' + str(len(cases)) + ' cases')

  def loadCasesFromPaths(self, casePaths):
    for index, casePath in enumerate(casePaths):
      self.cases.append(Case(casePath, index + 1))
    log.info('Loaded ' + str(len(self.cases)) + ' cases')

  def loadCasesFromDir(self, casesDir):
    casePaths = []
    for root, dirs, files in os.walk(casesDir):
      for i in files:
        if i.endswith('txt') and i.find('case') <> -1 :
          casePaths.append(os.path.join(root, i))
    self.loadCasesFromPaths(casePaths)

 #### get ####

  def getCasesByKey(self, key):
    cases = []
    for case in self.cases:
      if key in case.keyTypes:
        cases.append(case)
    return cases

  def getHomogenizedCases(self):
    homogenizedCases = deepcopy(self.cases)

    # add missing keys
    allKeys = self.getAllKeys()
    for case in homogenizedCases:
      for key in allKeys.difference(case.data.keys()):
        case.data[key] = '-1'

    # add missing key types
    allKeyTypes = self.getAllKeyTypes()
    for case in homogenizedCases:
      for key in allKeyTypes:
        case.keyTypes[key] = allKeyTypes[key]

    return homogenizedCases

  def getHomogenizedCasesByKeyValue(self, key, value, homogenizedCases = []):
    cases = []
    if len(homogenizedCases) == 0:
      homogenizedCases = self.getHomogenizedCases()
    for case in homogenizedCases:
      if (key in case.keyTypes) and (case.data[key] == value):
        cases.append(case)
    return cases

  def getAllKeys(self):
    keys = set([])
    for case in self.cases:
      keys = keys.union(case.data.keys())
    return keys

  def getAllKeyTypes(self):
    keyTypes = {}
    for case in self.cases:
      for key, value in case.keyTypes.items():
        keyTypes[key] = value
    return keyTypes

  def getAllExistingConditionsKeys(self):
    keys = set([])
    for case in self.cases:
      keys = keys.union(case.existingConditions)
    return keys

  def getAllNonexistingConditionsKeys(self):
    keys = set([])
    for case in self.cases:
      keys = keys.union(case.nonexistingConditions)
    return keys

  def getUniqueValuesByKey(self, key):
    uniqueValues = []
    for case in self.cases:
      if (key in case.keyTypes) and (case.data[key] not in uniqueValues):
        uniqueValues.append(case.data[key])
    return uniqueValues

  def getCasesByKeyValueSecondKey(self, key, value, key2):
    cases = []
    for case in self.cases:
      if (case.data[key] == value) and (key2 in case.data.keys()):
	    cases.append(case)
    return cases
	
 #### sort ####

  def getKeysSortedByMeans(self, keys):
    means = {}
    sortedKeys = []
    for key in keys:
      means[key] = len(self.getHomogenizedCasesByKeyValue(key, "1"))
    for key, value in sorted(means.items(), key=itemgetter(1), reverse=True):
      sortedKeys.append(key)
    return sortedKeys

 #### search/replace ####

  def substituteKey(self, oldKey, newKey):
    cases = self.getCasesByKey(oldKey)
    for case in cases:
      case.substituteKey(oldKey, newKey)
    log.info('Substituted "' + oldKey + '" with "' + newKey + '" in ' + str(len(cases)) + ' cases')

  def substituteKeysFromFile(self, keySubstitutionsFile):
    log.info('Loaded key substitutions file "' + keySubstitutionsFile + '"')
    fileData = open(keySubstitutionsFile).readlines()
    fileData = sanitize(fileData)
    fileData = [element.split(':') for element in fileData]
    fileData = [ [element[0].strip(), element[1].strip()] for element in fileData]

    for element in fileData:
      oldKey = element[0]
      newKey = element[1]

      cases = self.getCasesByKey(oldKey)
      for case in cases:
        case.substituteKey(oldKey, newKey)
      log.info('Substituted "' + oldKey + '" with "' + newKey + '" in ' + str(len(cases)) + ' cases')

  def searchKeys(self, key, value = ''):
    if value == '':
      cases = self.getCasesByKey(key)
    else:
      cases = self.getHomogenizedCasesByKeyValue(key, value)
    log.info('Searching for cases with "' + key + '"="' + value + '"...')
    for case in cases:
      log.info('\t' + case.path)

 #### dump ####

  def dumpCases(self):
    for case in self.cases:
      case.save()
    log.info('Dumped ' + str(len(self.cases)) + ' cases')

  def dumpGroupedKeys(self, keymap, keysPath):
    keyFile = open(keysPath, 'w')
    allKeymapKeys = set([])

    for group in keymap.groups:
      allKeymapKeys = allKeymapKeys.union(group.getAllKeys())
    remainingKeys = self.getAllKeys().difference(allKeymapKeys)

    for group in keymap.groups:
      keyFile.write('##### ' + group.name + ' #####\n')
      for key in group.getAllKeys():
        keyFile.write('  ' + key + '\n')

    keyFile.write('#### keys not found in keymap #####\n')
    for key in remainingKeys:
      keyFile.write('  ' + key + '\n')

    keyFile.close()
    log.info('Dumped ' + str(len(self.getAllKeys())) + ' keys (by keymap)')
    if len(remainingKeys) > 0:
      log.info(str(len(remainingKeys)) + ' keys not found in keymap')

  def dumpStataFiles(self, stataDumpDir):
    # dictionary file
    dictionaryFile = open(stataDumpDir + '/cases.dct', 'w')
    dictionaryFile.write('dictionary {\n')
    for key in sorted(self.getAllKeys()):
      dictionaryFile.write(self.getAllKeyTypes()[key] + ' ' + stataizeVariable(key) + ' "' + key + '"' + '\n')
    dictionaryFile.write('}\n')
    dictionaryFile.close()

    # novars file
    novarsFile = open(stataDumpDir + '/cases_novars.txt', 'w')
    for case in self.getHomogenizedCases():
      for key in sorted(self.getAllKeys()):
        novarsFile.write(stataizeValue(str(case.data[key])))
        novarsFile.write("\t")
      novarsFile.write('\n')
    novarsFile.close()

    log.info('Dumped stata dictionary and novars file to "' + stataDumpDir + '".')

 #### explore ####

  def searchKeys(self, key, value = ''):
    if value == '':
      cases = self.getCasesByKey(key)
    else:
      cases = self.getHomogenizedCasesByKeyValue(key, value)
    log.info('Searching for cases with "' + key + '"="' + value + '"...')
    for case in cases:
      log.info('\t' + case.path)
	  
  def explore(self):
    for key in self.getKeysSortedByMeans(self.getAllKeys()):
      log.info(key + '\t' + str(len(self.getHomogenizedCasesByKeyValue(key, "1"))))
	
	
	
	
#    autismCases = self.getCasesByKey('syndactyly')

#    cl = Caselist()
#    cl.loadCases(autismCases)

#    keys = cl.getKeysSortedByMeans(cl.getAllKeys())

#    for key in keys:
#      print key + '\t' + str(len(cl.getHomogenizedCasesByKeyValue(key, "1")))

#    for case in autismCases:
#      case.display()

 #### stats ####

 