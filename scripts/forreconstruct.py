#!/usr/bin/env python

from forrec import os
import argparse

def _init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--directory", action="store_true")
    group.add_argument("-i", "--image-file", action="store_true")
    #parser.add_argument("-
    return parser

def main():
    parser = _init_parser()
    args = parser.parse_args()
    if args.image_file:
        print "Not implemented yet!"
        return
    elif args.directory:
        dir = args.target
    analyzed_os = os.OS.create_from_directory(dir)

if __name__=="__main__":
    main()
