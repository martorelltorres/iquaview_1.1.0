#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Helpers for printing text in terminal with colors.
Color pretty print on the terminal.
"""

# ==============================================================================
# Console colors
BACKGRND = '\033[40m'
VIOLET = '\033[95m'
OKBLUE = '\033[94m'
WARNING = '\033[93m'
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'


# ==============================================================================
def printwarn(string):
    """
    Output string in different color.

    @param string: string to print
    @type string: string
    """
    #print('{:s}{:s}{:s}'.format(WARNING, string, ENDC))
    print(string)


def printerror(string):
    """
    Output string in different color.

    @param string: string to print
    @type string: string
    """
    #print('{:s}{:s}{:s}'.format(FAIL, string, ENDC))
    print(string)


def printdebug(string):
    """
    Output string in different color.

    @param string: string to print
    @type string: string
    """
    #print('{:s}{:s}{:s}'.format(OKBLUE, string, ENDC))
    print(string)


def printgreen(string):
    """
    Output string in different color.

    @param string: string to print
    @type string: string
    """
    #print('{:s}{:s}{:s}'.format(OKGREEN, string, ENDC))
    print(string)


def printviolet(string):
    """
    Output string in different color.

    @param string: string to print
    @type string: string
    """
    #print('{:s}{:s}{:s}'.format(VIOLET, string, ENDC))
    print(string)


def printbkgnd(string):
    """
    Output string in different color.

    @param string: string to print
    @type string: string
    """
    #print('{:s}{:s}{:s}'.format(BACKGRND, string, ENDC))
    print(string)


def printbold(string):
    """
    Output string in different color.

    @param string: string to print
    @type string: string
    """
    #print('{:s}{:s}{:s}'.format(BOLD, string, ENDC))
    print(string)


if __name__ == "__main__":
    printwarn("warning")
    printerror("error")
    printdebug("debug")
    printgreen("green")
    printviolet("violet")
    printbkgnd("background")
    printbold("bold")
