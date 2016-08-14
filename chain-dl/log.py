#!/usr/bin/env python3

"""
Basic logging functions (with colors though :D)
"""

import sys


HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def shiny(log, *args):
    print(OKBLUE, end='')
    print(log, *args, end='')
    print(ENDC)

def ok(log, *args):
    print("[ " + OKGREEN + "OK" + ENDC + " ] ", end='')
    print(log, *args)

def ok_shiny(log, *args):
    print("[ " + OKGREEN + "OK" + ENDC + " ] ", end='')
    print(OKGREEN, end='')
    print(log, *args, end='')
    print(ENDC)

def ko(log, *args):
    print("[ " + FAIL + "KO" + ENDC + " ] ", end='', file=sys.stderr)
    print(log, *args, file=sys.stderr)

def ko_shiny(log, *args):
    print("[ " + FAIL + "KO" + ENDC + " ] ", end='', file=sys.stderr)
    print(FAIL, end='', file=sys.stderr)
    print(log, *args, end='', file=sys.stderr)
    print(ENDC, file=sys.stderr)

def warn(log, *args):
    print("[ " + WARNING + "WARNING" + ENDC + " ] ", end='', file=sys.stderr)
    print(log, *args, file=sys.stderr)
