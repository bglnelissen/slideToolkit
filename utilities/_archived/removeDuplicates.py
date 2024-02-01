#!/usr/bin/env python3
# if running in py3, change the shebang, drop the next import for readability (it does no harm in py3)
# from __future__ import print_function   # py2 compatibility

# Reference: https://stackoverflow.com/a/36113168/4322048

print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("                                slideDuplicates: identify duplicate slides ")
print("")
print("* Version          : v1.0.0")
print("")
print("* Last update      : 2021-11-18")
print("* Written by       : Sander W. van der Laan | s.w.vanderlaan@gmail.com")
print("* Inspired by      : Todor Minakov")
print("")
print("* Description      : This script will check has by size, and content of files to identify duplicate images ")
print("                     for inspection and (manual) removal.")
print("")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# fix argument parser
# add in option check same study number, choose the most recent one, 
# make sure it's size is larger then 1Mb, and move all others
# to a new directory "_duplicates"
# add in option to rename files to 
# 1) include proper stain (requirement), 
# 2) remove spaces, dashes, and (), 
# only preserving files like AExxxx.[UMC/Txx-xxxxx].[STAIN].[ext]
# where [UMC/Txx-xxxxx] may not exist


# import required packages
from collections import defaultdict
import hashlib
import os
import sys

# parser = argparse.ArgumentParser(
# 	prog='slideDuplicates',
# 	description='This script will check has by size, and content of files to identify duplicate images for inspection and (manual) removal.',
# 	usage='slideDuplicates -i/--input -v/--verbose; for help: -h/--help',
# 	formatter_class=argparse.RawDescriptionHelpFormatter,
# 	epilog=textwrap.dedent("Copyright (c) 1979-2021 Sander W. van der Laan | s.w.vanderlaan-2@umcutrecht.nl"))
# 
# parser.add_argument('-s', '--studynr', help="Check files on studynumbers, i.e. AExxxx or AAAxxxx.", default="", type=str)
# parser.add_argument('-r', '--rename', help="Rename files to the form AExxxx.[UMC/Txx-xxxxx].[STAIN].[ext].", default="", type=str)
# parser.add_argument('-v', '--verbose', help="While writing images also display image properties.", default=False, action="store_true")
# 
# requiredNamed = parser.add_argument_group('required named arguments')
# 
# requiredNamed.add_argument('-i','--input',help="Input (directory containing files). Try: *.TIF or /path_to/images/*.ndpi.", nargs="*")
# 
# args = parser.parse_args()
# 
# if not args.input:
#     print("\nOh, computer says no! You must supply correct arguments when running a *** slideDuplicates ***!")
#     print("Note that -i/--input is required. Try: *.TIF or /path_to/images/*.ndpi.\n")
#     parser.print_help()
#     exit()
# 
# if len(args.input) > 1:  # bash has sent us a list of files
#     files = args.input
# else:  # user sent us a wildcard, need to use glob to find files
#     files = glob.glob(args.input[0])

def chunk_reader(fobj, chunk_size=1024):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk


def get_hash(filename, first_chunk_only=False, hash=hashlib.sha1):
    hashobj = hash()
    file_object = open(filename, 'rb')

    if first_chunk_only:
        hashobj.update(file_object.read(1024))
    else:
        for chunk in chunk_reader(file_object):
            hashobj.update(chunk)
    hashed = hashobj.digest()

    file_object.close()
    return hashed


def check_for_duplicates(paths, hash=hashlib.sha1):
    hashes_by_size = defaultdict(list)  # dict of size_in_bytes: [full_path_to_file1, full_path_to_file2, ]
    hashes_on_1k = defaultdict(list)  # dict of (hash1k, size_in_bytes): [full_path_to_file1, full_path_to_file2, ]
    hashes_full = {}   # dict of full_file_hash: full_path_to_file_string

    for path in paths:
        for dirpath, dirnames, filenames in os.walk(path):
            # get all files that have the same size - they are the collision candidates
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                try:
                    # if the target is a symlink (soft one), this will 
                    # dereference it - change the value to the actual target file
                    full_path = os.path.realpath(full_path)
                    file_size = os.path.getsize(full_path)
                    hashes_by_size[file_size].append(full_path)
                except (OSError,):
                    # not accessible (permissions, etc) - pass on
                    continue


    # For all files with the same file size, get their hash on the 1st 1024 bytes only
    for size_in_bytes, files in hashes_by_size.items():
        if len(files) < 2:
            continue    # this file size is unique, no need to spend CPU cycles on it

        for filename in files:
            try:
                small_hash = get_hash(filename, first_chunk_only=True)
                # the key is the hash on the first 1024 bytes plus the size - to
                # avoid collisions on equal hashes in the first part of the file
                # credits to @Futal for the optimization
                hashes_on_1k[(small_hash, size_in_bytes)].append(filename)
            except (OSError,):
                # the file access might've changed till the exec point got here 
                continue

    # For all files with the hash on the 1st 1024 bytes, get their hash on the full file - collisions will be duplicates
    for __, files_list in hashes_on_1k.items():
        if len(files_list) < 2:
            continue    # this hash of fist 1k file bytes is unique, no need to spend cpy cycles on it

        for filename in files_list:
            try: 
                full_hash = get_hash(filename, first_chunk_only=False)
                duplicate = hashes_full.get(full_hash)
                if duplicate:
                    print("Duplicates found (same size and content): {} and {}".format(filename, duplicate))
                else:
                    hashes_full[full_hash] = filename
            except (OSError,):
                # the file access might've changed till the exec point got here 
                continue


if __name__ == "__main__":
    if sys.argv[1:]:
        check_for_duplicates(sys.argv[1:])
    else:
        print("Please pass the paths to check as parameters to the script.")
        

print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("+ The MIT License (MIT)                                                                                           +")
print("+ Copyright (c) 1979-2021 Sander W. van der Laan | UMC Utrecht, Utrecht, the Netherlands                          +")
print("+                                                                                                                 +")
print("+ Permission is hereby granted, free of charge, to any person obtaining a copy of this software and               +")
print("+ associated documentation files (the \"Software\"), to deal in the Software without restriction, including       +")
print("+ without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell         +")
print("+ copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the        +")
print("+ following conditions:                                                                                           +")
print("+                                                                                                                 +")
print("+ The above copyright notice and this permission notice shall be included in all copies or substantial            +")
print("+ portions of the Software.                                                                                       +")
print("+                                                                                                                 +")
print("+ THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT         +")
print("+ LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO       +")
print("+ EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER       +")
print("+ IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR         +")
print("+ THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                                                      +")
print("+                                                                                                                 +")
print("+ Reference: http://opensource.org.                                                                               +")
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

