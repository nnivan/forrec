#!/usr/bin/env python

from forrec import os, vm
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--directory", action="store_true")
    group.add_argument("-i", "--image-file", action="store_true")
    args = parser.parse_args()
    if args.image_file:
        print "Not implemented yet!"
        return
    elif args.directory:
        dir = args.directory
    print "Done"

if __name__=="__main__":
    main()
