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
    os_string = analyzed_os.fetch_os_string()
    vm = VM(vm_type, vm_provider) # ("vagrant", "virtualbox")
    vm.create(os_string)
    reconstructed_os = OS.create_from_vm(vm)
    reconstructed_os.set_packages(target_packages) # TODO: target_opts
    #reconstructed_os.build()
    diffs = reconstructed_os.analyze_differences(analyzed_os)
    print diffs

if __name__=="__main__":
    main()
