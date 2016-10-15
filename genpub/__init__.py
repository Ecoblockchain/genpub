#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""genpub

Usage:
  genpub twitter <file> [--status=STATUS] [--reply=REPLY]
  genpub drive <file>
  genpub -h

Examples:

  genpub twitter <file>   Upload this file to twitter (and google drive)
  genpub drive <file>     Upload this file to google drive
  -h                      Show this screen.
  --version               Show version.
"""

__ALL__ = ['genpub']

from genpub.genpub import Genpub


def run():

  from docopt import docopt
  args = docopt(__doc__, version='genpub 0.0.2')
  main(args)

def main(args):

  from sys import stderr
  from sys import exit

  # print(args)
  # return

  try:
    with Genpub() as genpub:
      if args['drive']:
        res = genpub.pub_drive(
            args['<file>']
            )
        # print(res)
      elif args['twitter']:
        res = genpub.pub_twitter(
            args['<file>'],
            args['--status'],
            args['--reply']
            )
        # print(res)
      else:
        # this cant happen
        print('bad arguments, see: \ngenpub -h')

  except Exception as e:
    print(e, file=stderr)
    exit(1)


if __name__ == '__main__':
  run()

