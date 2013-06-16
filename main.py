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

import sys
import getopt
import os
import logging

from Case import Case
from Caselist import Caselist
from Manifest import Manifest
from Log import Log
from Keymap import Keymap 

__doc__ = '''Parses case file descriptions.
Syntax: python main.py [options] <manifestPath>  OR
        python main.py [options] <casesDir>

  required:
   -i <casesDir> or <manifestPath>

  load:
   -l <keymapFile>		load keymap

  search/replace:
   -S '<key>':'<value>'		search by key:value pair
   -r '<oldKey>:<newKey>'	substitute old key with new key
   -R '<keySubstitutionFile>	substitute old keys with new keys from file

  dump:
   -c				dump cases (save)
   -m <keysFile>		dump grouped keys
   -d <stataDir>		dump stata files
   -v <stataDir>		dump stata commands
   -e <excelDir>		dump excel data 
'''

class Usage(Exception):
  def __init__(self, message):
    self.message = message

def main(argv = None):
  if argv is None:
    argv = sys.argv
  try:
    try:
      options, arguments = getopt.getopt(argv[1:], "i:l:S:r:R:cm:d:v:e:")

      caselist = Caselist()
      manifest = Manifest()
      keymap = Keymap()

      # logging
      log = logging.getLogger('process')
      log.setLevel(logging.INFO)
      log.addHandler(logging.StreamHandler())

      # process options
      for option, argument in options:
        if option in ("-h", "--help"):
          print __doc__
          sys.exit(0)

        if option in ("-i", "--input"):
          if os.path.isfile(argument):
            caselist.loadCasesFromPaths(manifest.read(argument))
          elif os.path.isdir(argument):
            caselist.loadCasesFromDir(argument)
          else:
            print "Error: case files not loaded."
            sys.exit(0)

        #### load ####

        if option in ("-l", "--load-keymap"):
          keymap.load(argument)

        #### search/replace ####

        if option in ("-S", "--search-by-key-value"):
          keyValuePair = argument.split(':')
          key = keyValuePair[0]
          value = keyValuePair[1]
          caselist.searchKeys(key, value)         

        if option in ("-r", "--substitute-key"):
          substituteKeys = argument.split(':')
          caselist.substituteKey(substituteKeys[0], substituteKeys[1])

        if option in ("-R", "--subsitute-keys-from-file"):
          caselist.substituteKeysFromFile(argument)

        #### dump ####

        if option in ("-c", "--dump-cases"):
          caselist.dumpCases()

        if option in ("-m", "--dump-keys-by-keymap"):
          caselist.dumpGroupedKeys(keymap, argument)

        if option in ("-d", "--dump-stata"):
          caselist.dumpStataFiles(argument)

        if option in ("-v", "--dump-stata-commands"):
          keymap.dumpStataCommands(argument, caselist)

        if option in ("-e", "--dump-excel-data"):
          keymap.dumpExcelData(argument, caselist)

        #### etc ####
		
    except getopt.error, message:
       raise Usage(message)

  except Usage, error:
    print >>sys.stderr, error.message
    print >>sys.stderr, "for help use --help"
    return 2

if __name__ == "__main__":
  sys.exit(main())
