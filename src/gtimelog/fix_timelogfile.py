#!/usr/bin/env python
"""This script adds missing : to the timelog file.

requires every entry to be of the form

<timestamp> <project>-<task> <booking text>

and creates timelog-out.txt with entries containing a : after the task to mark
project and task as a category

<timestamp> <project>-<task>: <booking text>

the following phrases can be used to start a new day:
* arrived
* started
"""


import re
import sys


SOURCE_FILE = 'timelog.txt'
OUT_FILE = 'timelog-out.txt'


pattern = r'(^[-0-9]* \d+:\d+: )([\S]*-[\S]*)( .*)'
datepattern = r'(^[-0-9]* \d+:\d+: )(.*)'

with open(OUT_FILE, 'w') as out:
  with open(SOURCE_FILE, 'r') as f:
      for line in f:

          dateline = re.search(datepattern, line)
          if not dateline or line.strip().endswith('**'):
              #no error for comments, or slacking entries
              out.write(line)
              continue

          else:
              if 'started' == dateline.groups()[1] or 'arrived' == dateline.groups()[1]:
                 out.write(line)
                 continue


              result = re.match(pattern, line)
              if result is None:
                  print "skip " + line
                  out.write(line)
              else:
                  date, cat, comment = result.groups()
                  if cat.endswith(':'):
                      #entry that has colon already
                      out.write("%s%s%s\n" % result.groups())
                  else:
                      out.write("%s%s:%s\n" % result.groups())
