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

import re

def removeCommentLines(contents):
  commentToken = '#'
  newContents = []
  for line in contents:
    if line.startswith(commentToken):
      continue
    else:
      newContents.append(line)
  return newContents

def removeEmptyLines(contents):
  newContents = []
  for line in contents:
    if not line.strip():
      continue
    else:
      newContents.append(line)
  return newContents

def sanitize(dirtyList):
  cleanList = []
  dirtyTokens = ['\n', ' ', '']
  for token in dirtyTokens:
    while token in dirtyList:
      itemNumber = dirtyList.index(token)
      del dirtyList[itemNumber]
  for item in dirtyList:
    cleanList.append(item.strip())
  return cleanList

def convertBirthWeight(birthWeightString):
  number = float(birthWeightString[0 : len(birthWeightString) - 1])
  units = birthWeightString[len(birthWeightString) - 1]
  if units == 'g':
    return number
  return -9999

def convertLength(lengthString):
  number = float(lengthString[0 : len(lengthString) - 2])
  units = lengthString[len(lengthString) - 2] + lengthString[len(lengthString) - 1]
  if units == 'cm':
    return number
  return -9999


def convertHeadCircumference(headCircumferenceString):
  number = float(headCircumferenceString[0 : len(headCircumferenceString) - 2])
  units = headCircumferenceString[len(headCircumferenceString) - 2] + headCircumferenceString[len(headCircumferenceString) - 1]
  if units == 'cm':
    return number
  return -9999

def convertAgeString(ageString):
  number = float(ageString[0 : len(ageString) - 1])
  units = ageString[len(ageString) - 1]
  if units == 'y':
    return number
  elif units == 'm':
    return number / 12
  elif units == 'd':
    return number / 365
  return -9999

def convertGestationString(gestationString):
  m = re.search('\D', gestationString)
  units = m.group(0)
  number = int(gestationString.replace(units, ''))
  if units == 'w':
    return number
  return -9999  

def stataizeVariable(variable):
  dirtyTokens = [' ', '-', '/', '(', ')', "'"]
  for token in dirtyTokens:
    variable = variable.replace(token, '_')
  if len(variable) > 25:
    variable = variable[0:24]
  return variable

def stataizeValue(value):
  dirtyTokens = [' ']
  for token in dirtyTokens:
    value = value.replace(token, '_')
  return value

def sortDictionary(dictionary):
  newDictionary = {}
  sortedKeys = dictionary.keys()
  sortedKeys.sort()
  for key in sortedKeys:
    newDictionary[key] = dictionary[key]
  return newDictionary

