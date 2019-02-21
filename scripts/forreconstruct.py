#!/usr/bin/env python

from forrec import os
from forrec import vm
from forrec.analysis import analyze_differences
from forrec.analysis import print_differences
from forrec.analysis import outfile_differences
import argparse

VAGRANT_VM_FOLDER_NAME = '.'
FOLDERS_TO_CHECK = ['/usr/bin']

def _init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--directory", action="store_true")
    group.add_argument("-i", "--image-file", action="store_true")
    verb = parser.add_mutually_exclusive_group()
    verb.add_argument("-v", "--verbose", action="count", default=2)
    verb.add_argument("-q", "--quiet", action="count", default=0)
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'))
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
    print "analyzed_os"
    os_string = analyzed_os.fetch_os_string()
    print "os_string -", os_string
    target_packages = analyzed_os.extract_packages()
    print "target_packages"
    cksum_list_analyzed_os = analyzed_os.fetch_cksum(FOLDERS_TO_CHECK)
    # print "cksum_list_analyzed_os:\n", cksum_list_analyzed_os

    virtual_os = vm.VM(VAGRANT_VM_FOLDER_NAME)
    print "virtual_os"
    virtual_os.create(os_string)
    print "virtual_os.create"
    reconstructed_os = os.OS.create_from_vm(VAGRANT_VM_FOLDER_NAME, virtual_os) # virtual_os.create(os_string)
    print "reconstructed_os"
    reconstructed_os.set_packages(target_packages) # virtual_os.install_packages(target_packages)
    print "reconstructed_os.set_packages"

    cksum_list = reconstructed_os.fetch_cksum(FOLDERS_TO_CHECK)
    print "cksum_list"
    diffs = analyze_differences(cksum_list_analyzed_os, cksum_list)

    # diffs = [["ok", ["0", "0", "okfile"], ["0", "0", "okfile"]], ["wr", ["0", "0", "wrfile"], ["1", "1", "wrfile"]], ["ex", ["3", "3", "exfile"], ["3", "3", "exfile"]], ["ms", ["4", "4", "msfile"], ["4", "4", "msfile"]]]

    print_differences(diffs, args.verbose - args.quiet)

    if args.outfile:
        outfile_differences(args.outfile, diffs)

    # TODO: remove this later:
    # virtual_os.client.close()

    print "End\n"


    # reconstructed_os = OS.create_from_vm("vm_machine"virtual_os)
    # reconstructed_os.set_packages(target_packages) # TODO: target_opts
    # reconstructed_os.build()
    # diffs = reconstructed_os.analyze_differences(analyzed_os)
    # print diffs

if __name__=="__main__":
    main()
