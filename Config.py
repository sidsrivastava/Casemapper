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

import ConfigParser

ignorableGroups = []
nonnumericKeys = []
internalKeys = []
commonKeys = []

def load(path):
  global ignorableGroups
  global nonnumericKeys
  global internalKeys
  global commonKeys

  # open config file
  parser = ConfigParser.ConfigParser()
  parser.read(path)

  ignorableGroups = [x.strip() for x in parser.get("Keymap", "ignorableGroups").split(',')]
  internalKeys = [x.strip() for x in parser.get("Cases", "internalKeys").split(',')]
  commonKeys = [x.strip() for x in parser.get("Cases", "commonKeys").split(',')]
  nonnumericKeys = [x.strip() for x in parser.get("Cases", "nonnumericKeys").split(',')]
  
#  internalKeys = ['id']
#  commonKeys = ['paper', 'sex', 'age', 'syndrome']
#  ignorableGroups = ['identifier', 'demographics', 'genetics', 'growth']
#  nonnumericKeys = []