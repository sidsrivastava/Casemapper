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

import operator
import logging
from utilities import *

internalKeys = ['id']
commonKeys = ['paper', 'sex', 'age', 'mutation', 'protein change']
defaultUnits = {'age':'y'}

# log
log = logging.getLogger('process')

class Case:

  def __init__(self, casePath, caseID):
    self.ID = caseID
    self.path = casePath
    self.data = {}

    # metadata
    self.keyTypes = {}
    self.existingConditions = []
    self.nonexistingConditions = []
    self.untransformedData = {}

    self.load()

  def display(self):
    print self.path
    for key, value in self.data.iteritems():
      print str(key) + '\t' + str(value)
    print '\n'

  def load(self):
    # read file data
    fileData = open(self.path).readlines()
    fileData = sanitize(fileData)
    fileData = [element.split(':') for element in fileData]
    fileData = [ [element[0].strip(), element[1].strip()] for element in fileData]

    # parse elements
    for element in fileData:
      if element[0] == '+':
        self.existingConditions = element[1].split(',')
      elif element[0] == '-':
        self.nonexistingConditions = element[1].split(',')
      elif element[0] == 'age':
        self.data[element[0]] = convertAgeString(element[1])
        self.keyTypes[element[0]] = 'float'
      elif element[0] <> '':
        self.data[element[0]] = element[1]
        self.keyTypes[element[0]] = 'str244'

    # process conditions
    self.existingConditions = sanitize(self.existingConditions)
    self.nonexistingConditions = sanitize(self.nonexistingConditions)
    for condition in self.existingConditions:
       self.data[condition.strip()] = '1'
       self.keyTypes[condition.strip()] = 'int'
    for condition in self.nonexistingConditions:
      self.data[condition.strip()] = '0'
      self.keyTypes[condition.strip()] = 'int'

    # assign an ID to the case
    self.data['id'] = self.ID
    self.keyTypes['id'] = 'int'

  def save(self):
    caseFile = open(self.path, 'w')
    # write common keys
    for key in commonKeys:
      if key in self.data.keys():
        caseFile.write(key + ': ' + str(self.data[key]))
        # add in units where appropriate
        if key in defaultUnits.keys(): caseFile.write(defaultUnits[key])
        caseFile.write('\n')

    # write existing conditions
    if len(self.existingConditions) > 0:
      caseFile.write('+: ')
      for index, condition in enumerate(self.existingConditions):
        caseFile.write(condition)
        # add in units where appropriate
        if condition in defaultUnits.keys(): caseFile.write(defaultUnits[condition])
        if index < len(self.existingConditions) - 1:
          caseFile.write(', ')
      caseFile.write('\n')

    # write non-existing conditions
    if len(self.nonexistingConditions) > 0:
      caseFile.write('-: ')
      for index, condition in enumerate(self.nonexistingConditions):
        caseFile.write(condition)
        # add in units where appropriate
        if condition in defaultUnits.keys(): caseFile.write(defaultUnits[condition])
        if index < len(self.nonexistingConditions) - 1:
          caseFile.write(', ')
      caseFile.write('\n')

    # write untransformed elements
    for key, value in self.untransformedData.iteritems():
       caseFile.write(key + ': ' + str(value))
       if key in defaultUnits.keys(): caseFile.write(defaultUnits[key])
       caseFile.write('\n')

    # write remaining elements
    for key, value in self.data.iteritems():
      if (not key in commonKeys) and (not key in self.existingConditions) and (not key in self.nonexistingConditions) and (not key in internalKeys) and (not key in self.untransformedData.keys()):
        caseFile.write(key + ': ' + str(value))
        # add in units where appropriate
        if key in defaultUnits.keys(): caseFile.write(defaultUnits[key])
        caseFile.write('\n')

    caseFile.close()

  def substituteKey(self, oldKey, newKey):
    if oldKey in self.existingConditions:
      self.existingConditions.append(newKey)
      self.existingConditions.remove(oldKey)
    if oldKey in self.nonexistingConditions:
      self.nonexistingConditions.append(newKey)
      self.nonexistingConditions.remove(oldKey)
    for key in self.data.keys():
      if key == oldKey:
        self.data[newKey] = self.data[oldKey]
        self.keyTypes[newKey] = self.keyTypes[oldKey]
        del self.data[oldKey]
        del self.keyTypes[oldKey]

