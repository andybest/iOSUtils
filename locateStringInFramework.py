#!/usr/bin/python

""" Utility to search through iOS Private Frameworks for symbols
    matching the input string
"""

import os
import subprocess
from optparse import OptionParser

def parse_arguments():
    parser = OptionParser()
    parser.add_option("-i", "--case-insensitive", dest="caseInsensitive",
                              action="store_true",
                              default=False,
                              help="make matching case insensitive")
    parser.add_option("-f", "--framework-directory", dest="frameworkDirectory",
                              default="./",
                              help="location of framework directory to search. (Default is the current working directory)")

    (options, args) = parser.parse_args()
    return options, args 


def do_search(opts, args):
    files = os.listdir(opts.frameworkDirectory)
    libs = get_lib_list(files, opts.frameworkDirectory)
    
    for p in libs:
        symbols = find_symbols(p, args[0], caseInsensitive=opts.caseInsensitive)

        if len(symbols) > 0:
            print "Found symbols in " + p + " :"
            for s in symbols:
                print "\t" + s
            print "---------------\n"


def get_lib_list(files, fileDir):
    libs = []

    for f in files:
        fullPath = fileDir + "/" + f
        if os.path.isdir(fullPath):
            if(f.lower().endswith(".framework")):
                libName = os.path.splitext(f)[0]
                libs.append(fileDir + "/" + f + "/" + libName)

    return libs


def find_symbols(path, searchTerm, caseInsensitive=False):
    symbols = []

    cmd = "nm " + path
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        if caseInsensitive:
            if searchTerm.lower() in line.lower():
                symbols.append(line.rstrip('\n'))
        else:
            if searchTerm in line:
                symbols.append(line.rstrip('\n'))
    
    retval = p.wait()
    
    return symbols

if __name__ == '__main__':
    (opts, args) = parse_arguments()
    do_search(opts, args) 
