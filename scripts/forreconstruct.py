#!/usr/bin/env python3

from forrec import forrec_os
from forrec import vm
from forrec.analysis import analyze_differences
from forrec.analysis import print_differences
from forrec.analysis import outfile_differences
import argparse

import code

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
    # parser.add_argument("-
    return parser


def main():
    parser = _init_parser()
    args = parser.parse_args()
    if args.directory:
        fs_dir = args.target
    else:
        print("Not implemented yet!")
        return

    analyzed_os = forrec_os.OS.create_from_directory(fs_dir)
    print("Filesystem:\t", fs_dir)

    os_string = analyzed_os.get_os_string()
    print("OS string:\t", os_string)

    investigator = vm.VM("investigator")
    investigator.create(os_string, analyzed_fs=fs_dir)

    packages = analyzed_os.get_packages(investigator)
    print("Packages:\t", len(packages))

    reconstructed_os = vm.VM("reconstructed")
    reconstructed_os.create(os_string, vbguest=False)

    analyzed_os.set_packages(packages, reconstructed_os)
    pass


if __name__ == "__main__":
    main()
