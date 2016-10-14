#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""genpub

Usage:
  genpub <file>
  genpub -h

Examples:

  genpub         Nothing
  genpub file    Store most recent image in directory 'dir'.
  -h             Show this screen.
  --version      Show version.
"""

__ALL__ = ['genpub']

from genpub.genpub import Genpub


def run():

  from docopt import docopt
  args = docopt(__doc__, version='genpub 0.0.1')
  main(args)

def main(args):

  from sys import stderr
  from sys import exit

  # print(args)
  try:
    with Genpub() as genpub:
      genpub.pub(args['<file>'])

  except Exception as e:
    print(e, file=stderr)
    exit(1)


if __name__ == '__main__':
  run()

