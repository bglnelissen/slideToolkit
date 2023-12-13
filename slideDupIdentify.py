#!/usr/bin/env python3

"""
slideDupIdentify

This script identifies and organizes duplicate files based on specified criteria,
such as study type and stain name. It prioritizes duplicates according to certain 
rules. It provides options to output information about the duplicates
and log statistics.

Usage:
python slideDupIdentify.py --studytype AE --stain CD34 --output duplicate_files

Options:
    --image-folder, -i Specify the folder where images are located (default: current directory). Required.
    --studytype, -t    Specify the study type prefix, e.g., AE. Required.
    --stain, -s        Specify the stain name, e.g., CD34. Required.
    --out_file, -o     Specify the output file name (without extension) to write duplicate information. Required.
    --log_file, -l     Write statistics to a log file. Optional.
    --dry_run, -d      Perform a dry run (report in the terminal, no actual file operations. Optional.
    --verbose, -V      Print the number of duplicate samples identified. Optional.
    --help, -h         Print this help message and exit. Optional.
    --version, -v      Print the version number and exit. Optional.
"""
# Version information
VERSION_NAME = 'slideDupIdentify'
VERSION = '1.0.0'
COPYRIGHT = 'Copyright 1979-2023. Sander W. van der Laan | s.w.vanderlaan@gmail.com | https://vanderlaanand.science.'
COPYRIGHT_TEXT = f'\nThe MIT License (MIT). \n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and \nassociated documentation files (the "Software"), to deal in the Software without restriction, \nincluding without limitation the rights to use, copy, modify, merge, publish, distribute, \nsublicense, and/or sell copies of the Software, and to permit persons to whom the Software is \nfurnished to do so, subject to the following conditions: \n\nThe above copyright notice and this permission notice shall be included in all copies \nor substantial portions of the Software. \n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, \nINCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR \nPURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS \nBE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, \nTORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE \nOR OTHER DEALINGS IN THE SOFTWARE. \n\nReference: http://opensource.org.'

# Import required packages
import os
import argparse
from argparse import RawTextHelpFormatter
import shutil
import hashlib
import random
import time
from collections import defaultdict, Counter

# Check if the required packages are installed
# try:
#     import polars as pl
# except ModuleNotFoundError:
#     ### This part is a security concern
#     # import subprocess     
#     # subprocess.run(["pip", "install", 'polars'])
#     # import polars as pl
#     ### This is an alternative.
#     print("Please install polars 'pip install polars' and try again.")
#     raise

# Calculate the checksum of a file
def calculate_checksum(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

# Get the priority of a file based on the specified criteria
def get_file_priority(file_info):
    date, file_type = file_info.split('.')[1:3]
    if file_type == 'ndpi':
        return 'diff_date_type_kept_ndpi'
    return 'same_date_diff_type_kept_ndpi' if date == current_date else 'same_checksum_random' if checksum in checksums else 'diff_date_same_type_newest'

# Move the file to the duplicate folder
def move_to_duplicates(file_path, duplicate_folder, dry_run=False):
    duplicate_file = os.path.join(duplicate_folder, os.path.basename(file_path))
    if not dry_run:
        shutil.move(file_path, duplicate_file)
    return duplicate_file

# Write the priority information to a file
def write_priority_info(output_file, priority_info, dry_run=False):
    if not dry_run:
        with open(output_file, 'w') as f:
            f.write("study_number\tfilename\tchecksum\tfilesize\tfiledate\tpriority\n")
            for info in priority_info:
                f.write('\t'.join(map(str, info)) + '\n')


# Main function
def main():
    parser = argparse.ArgumentParser(description='Identify and move duplicate files based on specified criteria.')
    parser = argparse.ArgumentParser(description=f'''
        + {VERSION_NAME} v{VERSION} +

        Identify and move duplicate image files based on specified criteria.
        This script identifies and organizes duplicate files based on specified criteria, such as `--output` for the
        output file name, study type (`--studytype`), stain name (`--stain`). It prioritizes duplicates according to 
        certain rules. It provides options (`--verbose`) to output information about the duplicates
        and log statistics using `--log`.
        
        Example usage:
        python slideDupIdentify.py --studytype AE --stain CD34 --output duplicate_files
        ''',
        epilog=f'''
        + v{COPYRIGHT} +''', 
        formatter_class=RawTextHelpFormatter)
    parser.add_argument('--image_folder', '-i', required=True, help='Specify the folder where images are located (default: current directory). Required.')
    parser.add_argument('--studytype', '-t', required=True, help='Specify the study type prefix, e.g., AE. Required.')
    parser.add_argument('--stain', '-s', required=True, help='Specify the stain name, e.g., CD34. Required.')
    parser.add_argument('--out_file', '-o', required=True, help='Specify the output file name (without extension) to write duplicate information. Required.')
    parser.add_argument('--verbose', '-v', action='store_true', help='Print the number of duplicate samples identified. Optional.')
    parser.add_argument('--log_file', '-l', action='store_true', help='Write statistics to a log file. Optional.')
    parser.add_argument('--dry_run', '-d', action='store_true', help='Perform a dry run (report in the terminal, no actual file operations. Optional.')
    parser.add_argument('--version', '-V', action='version', version=f'%(prog)s {VERSION}.')
    args = parser.parse_args()

    # Check if the image folder exists
    os.chdir(args.image_folder)  # Change current working directory to the image folder

    # Start the timer
    start_time = time.time()

    # Create the duplicate folder
    duplicate_folder = os.path.join(args.stain, '_duplicates')
    os.makedirs(duplicate_folder, exist_ok=True)

    # Set some variables
    unique_samples = set()
    checksums = set()
    priority_info = []

    multiplicity_info = defaultdict(int)

    # Loop through the files
    for file_name in os.listdir('.'):
        if file_name.startswith(args.studytype) and args.stain in file_name:
            study_number, file_info = file_name.split('.', 1)
            unique_samples.add(study_number)

            file_path = os.path.abspath(file_name)
            checksum = calculate_checksum(file_path)

            if checksum in checksums:
                multiplicity_info[study_number] += 1

                current_date = file_info.split('.')[1]

                priority = get_file_priority(file_info)
                priority_info.append((study_number, file_name, checksum, os.path.getsize(file_path), current_date, priority))

                duplicate_file = move_to_duplicates(file_path, duplicate_folder, args.dry_run)

                if args.verbose:
                    print(f"Duplicate found: {file_name} -> {duplicate_file}")

            checksums.add(checksum)

    # Write the priority information to a file
    write_priority_info(os.path.join(duplicate_folder, args.out_file + '.priorities.txt'), priority_info, args.dry_run)

    # Write the statistics to a log file
    if args.log_file:
        with open(os.path.join(duplicate_folder, args.out_file + '.statistics.log'), 'w') as log_file:
            log_file.write(f"Total unique samples for stain {args.stain}: {len(unique_samples)}\n")
            log_file.write(f"Total multiplicity files found: {len(multiplicity_info)}\n")
            for multiplicity, count in multiplicity_info.items():
                log_file.write(f"Multiplicity {multiplicity}: {count}\n")

            log_file.write(f"Total duplicates found: {len(priority_info)}\n")
            for priority, count in Counter(priority_info):
                log_file.write(f"Priority {priority}: {count}\n")

            log_file.write(f"Script execution time: {time.time() - start_time} seconds\n")

# Run the main function    
if __name__ == '__main__':
    main()

# Print the version number
print(f'{VERSION_NAME} v{VERSION} | {COPYRIGHT}')
print(f'{COPYRIGHT_TEXT}')

# End of file