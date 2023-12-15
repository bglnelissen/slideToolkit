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
    --force, -f        Force overwrite if the output file already exists. Optional.
    --dry_run, -d      Perform a dry run (report in the terminal, no actual file operations. Optional.
    --verbose, -V      Print the number of duplicate samples identified. Optional.
    --help, -h         Print this help message and exit. Optional.
    --version, -v      Print the version number and exit. Optional.
"""

# Version information
VERSION_NAME = 'slideDupIdentify'
VERSION = '1.0.0'
COPYRIGHT = 'Copyright 1979-2023. Tim S. Peters & Sander W. van der Laan | s.w.vanderlaan@gmail.com | https://vanderlaanand.science.'
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
from datetime import datetime
from datetime import timedelta
import pandas as pd

# Calculate the checksum of a file
def calculate_checksum(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

# Get the file extension
def get_study_and_remaining(file_name):
    # Split the filename and extension
    file_basename, file_extension = os.path.splitext(file_name)
    
    # Split the filename into studytype + studynumber and the remaining part
    file_basename_info = file_basename.split('.', 1)
    
    # Extract studytype + studynumber, remaining part, and extension
    if len(file_basename_info) == 2:
        studytype_and_studynumber, file_remaining_part = file_basename_info
    else:
        studytype_and_studynumber = file_basename_info[0]
        file_remaining_part = ''
    
    return studytype_and_studynumber, file_remaining_part, file_extension

# Move the file to the duplicate folder
def move_to_duplicates(file_path, duplicate_folder, priority, dry_run=False, verbose=False):
    if not dry_run:
        if priority:
            duplicate_file = os.path.join(duplicate_folder, os.path.basename(file_path))
            if verbose:
                print(f"  - {file_path} > {duplicate_file} (prioritized)")
            shutil.move(file_path, duplicate_file)
        else:
            duplicate_file = os.path.join(duplicate_folder, '_backup_duplicates', os.path.basename(file_path))
            if verbose:
                print(f"  - {file_path} > {duplicate_file} (not prioritized)")
            shutil.move(file_path, duplicate_file)

    return duplicate_file

# Function to preprocess fileype for prioritization
def process_prioritazation(metadata_df, verbose=False):
    study_numbers = defaultdict()

    # Get the different file metadata per study_number
    for snr in metadata_df['study_number'].unique():
        study_number_df = metadata_df.loc[metadata_df['study_number'] == snr]
        study_numbers[snr] = study_number_df

    for study_number, study_number_df in study_numbers.items():
        print(f"> processing {study_number} with {len(study_number_df)} files")
        if study_number_df['filetype'].nunique() > 1:
            # If there are different filetypes, only prioritize the .ndpi files
            ndpi_files = study_number_df.loc[study_number_df['filetype'] == '.ndpi']
            prioritized_file = prioritize_files(ndpi_files)
        else:
            # There is no diffenece in filetype, so prioritize whole list
            prioritized_file = prioritize_files(study_number_df)
        
        reason = f"{list(prioritized_file.values())[0]['filetype'].replace('.','')}_{list(prioritized_file.values())[1]}"
        filename= list(prioritized_file.values())[0]['filename']
        if verbose:
            print(f' prioritized file: {filename} - reason: {reason}')

        # Add prioritazation reason to dataframe
        metadata_df.loc[metadata_df['filename'] == filename, 'priority'] = reason

    return metadata_df

# Function returning a prioritized list of the same study_number
def prioritize_files(files):
    if len(files) == 1:
        return {'metadata': files.iloc[0], 'priority': 'keep_this_one'}    

    if files['file_mod_date'].nunique() > 1:
        # Sort files by mod date
        files_sorted_by_date = files.sort_values(by='file_mod_date', ascending=[False])
        # Different creation date > keep latest file
        kept_file = files_sorted_by_date.iloc[0]
        prioritized_file = {'metadata': kept_file, 'priority': 'different_date_kept_latest'}
    else:
        # Same date, same type
        if files['checksum'].nunique() > 1:
            # Same date, same type, different checksum > keep biggest
            files_same_type = files.sort_values(by=['filesize'], ascending=[False])
            kept_file = files_same_type.iloc[0]
            prioritized_file = {'metadata': kept_file, 'priority': 'same_date_same_type_diff_checksum_biggest'}
        elif files['checksum'].nunique() == 1:
            # Same date, same type, same checksum > keep first one
            kept_file = files.iloc[0]
            prioritized_file = {'metadata': kept_file, 'priority': 'same_date_same_type_same_checksum_keep_this_one'}
        else:
            # None of the above apply
            prioritized_file = {'metadata': None, 'priority': 'cannot_assign_priority'}

    return prioritized_file

# Main function
def main():
    parser = argparse.ArgumentParser(description=f'''
+ {VERSION_NAME} v{VERSION} +

Identify and move duplicate image files based on specified criteria.
This script identifies and organizes duplicate files based on specified criteria, such as `--output` for the
output file name, study type (`--study_type`), stain name (`--stain`). It prioritizes duplicates according to 
certain rules. It provides options (`--verbose`) to output information about the duplicates and log statistics 
using `--log`.

Images are expected to be of the form `study_typestudy_number.[additional_info.]stain.[random_info.]file_extension`, 
e.g., `AE1234.T01-12345.CD34.ndpi`, where `AE` is the `study_type`, `1234` is the `study_number`, 
`T01-12345` is the `additional_info` and optional, `CD34` is the stain name, and `ndpi` is the `file_extension`. 
The `random_info` is optional and can be any random string of characters, e.g. `2017-12-22_23.54.03`. The 
`file_extension` is expected to be `ndpi` or `TIF` for the original image files. 

The script will move all files with the same `study_number` and `stain` name to the duplicate folder. It will 
prioritize the files based on the following criteria:
- There is a ndpi > keep ndpi, `keep_this_one`
- Different creation date > keep latest file, `different_date_kept_latest`
- Same date, different type > keep ndpi, `same_date_diff_type_kept_ndpi`
- Same date, same type, different checksum > keep biggest, `same_date_same_type_diff_checksum_biggest`
- Same date, same type, same checksum > keep first one, `same_date_same_type_same_checksum_keep_this_one`
- When none of the above apply > `cannot_assign_priority`

Example usage:
python slideDupIdentify.py --study_type AE --stain CD34 --output duplicate_files [options --force --dry_run --verbose]
        ''',
        epilog=f'''
+ {VERSION_NAME} v{VERSION}. {COPYRIGHT} \n{COPYRIGHT_TEXT}+''', 
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--image_folder', '-i', required=True, help='Specify the folder where images are located (default: current directory). Required.')
    parser.add_argument('--study_type', '-t', required=True, help='Specify the study type prefix, e.g., AE. Required.')
    parser.add_argument('--stain', '-s', required=True, help='Specify the stain name, e.g., CD34. Required.')
    parser.add_argument('--out_file', '-o', required=True, help='Specify the output file name (without extension) to write duplicate information. Required.')
    parser.add_argument('--force', '-f', action='store_true', help='Force overwrite if the output file already exists. Optional.')
    parser.add_argument('--dry_run', '-d', action='store_true', help='Perform a dry run (report in the terminal, no actual file operations. Optional.')
    parser.add_argument('--debug', '-D', action='store_true', help='Print debug information. Optional.')
    parser.add_argument('--verbose', '-v', action='store_true', help='Print the number of duplicate samples identified. Optional.')
    parser.add_argument('--version', '-V', action='version', version=f'%(prog)s {VERSION}.')
    args = parser.parse_args()

    # Set the debug variable
    debug=args.debug
    
    # Start the timer
    start_time = time.time()

    print(f"+ {VERSION_NAME} v{VERSION} +")
    print(f"\nIdentify and move multiplicate image files based on specified criteria for:\n> study_type: {args.study_type}\n> stain: {args.stain}")
    
    if debug:
        print(f"\n>>> Debugging Mode: ON <<<\n")
    # Check if the image folder exists
    image_folder = args.image_folder
    stain_image_folder = os.path.join(image_folder, args.stain)
    if not os.path.exists(image_folder):
        print(f"Error: image folder '{image_folder}' does not exist.")
        exit(1)
    # Check that the stain folder exists and is not empty
    if not os.path.exists(stain_image_folder):
        print(f"Error: image/stain folder '{stain_image_folder}' does not exist.")
        exit(1)
    
    # Change current working directory to the stain folder
    os.chdir(stain_image_folder)
    
    # Check content of the image folder
    if not os.listdir():
        print(f"Error: image folder '{stain_image_folder}' is empty.")
        exit(1)

    # Create the (backup) duplicate folders
    duplicate_folder = os.path.join('.','_duplicates')
    os.makedirs(duplicate_folder, exist_ok=True)
    backup_duplicate_folder = os.path.join(duplicate_folder, '_backup_duplicates')
    os.makedirs(backup_duplicate_folder, exist_ok=True)

    # Check if the output file exists
    output_file_path = os.path.join(duplicate_folder, args.out_file + '.' + args.study_type + '.' + args.stain + '.metadata.csv')
    log_file_path = os.path.join(duplicate_folder, args.out_file + '.' + args.study_type + '.' + args.stain + '.metadata.log')
    if os.path.exists(output_file_path) and not args.force:
        print(f"\nOops, the output file [{output_file_path}] already exists. Did you run this multiplicate check before?")
        print(f"Double back, double check, and try again. If you ran it before, you can find the output file in the")
        print(f"duplicate folder [{duplicate_folder}] and a printout in the terminal below.\n")
        print(f"{output_file_path}")
        df = pd.read_csv(output_file_path, verbose=True)
        print(f"{df}")
        del df
        print(f"\nUse the --force option to overwrite the output file. \nExiting...")
        exit(1)
    
    print(f'> Duplicate folder created ({duplicate_folder}).\n')

    # Set some variables
    study_numbers_count = defaultdict(int)
    duplicate_study_numbers = set()
    multiplicity_df = pd.DataFrame(
        {
            "study_number": [],
            "filename": [],
            "file_path": [],
            "file_name_info": [],
            "checksum": [],
            "filesize": [],
            "file_create_date": [],
            "file_mod_date": [],
            "filetype": [],
            "priority": []
        }
    )
    unique_samples = set()
    remaining_unique_samples = []

    # Loop through the files and identify the duplicates and unique files
    print(f"Starting searching for multiplicate images.")
    if args.verbose:
        print(f"Listing all images:")
    for file_name in os.listdir('.'):
        if file_name.startswith(args.study_type) and args.stain in file_name:
            # Get the study number and file information
            file_path = os.path.abspath(file_name)
            # we are not using file_name_info, file_name_extension, but keep it for now
            study_number, file_name_info, file_name_extension = get_study_and_remaining(file_name) 
            
            # Counting the number of occurrences of study numbers
            study_numbers_count[study_number] += 1
            # Report the file name
            if args.verbose:
                print(f"> {study_number} ({file_name})") 

    print(f"\nIdentifying multiplicates...")
    
    # Identify study numbers with duplicates
    for study_number, count in study_numbers_count.items():
        if count == 1:
            # Keep track of unique study numbers
            unique_samples.add(study_number)
        elif count > 1:
            # Keep track of study numbers with duplicate files
            duplicate_study_numbers.add(study_number)
            print(f"> {study_number} ({count} images)")

    remaining_unique_samples = len(unique_samples)

    print(f"\nMultiplicates found:")
    print(f"> {len(duplicate_study_numbers)} studynumber(s) with multiplicates found")
    print(f"> Multiplicates for studynumber(s): {duplicate_study_numbers}")

    # Report the number of unique and total images found
    print(f"\nReporting the number of unique and total images found:")
    print(f"> {len(study_numbers_count)} unique images found based on studynumbers")
    print(f"> {sum(study_numbers_count.values())} total images found {dict(study_numbers_count)}")
    
   # Collect metadata for prioritization processing
    print(f"\nProcessing studynumber, collecting metadata for prioritization...")
    for file_name in os.listdir('.'):
        if file_name.startswith(args.study_type) and args.stain in file_name:
            # Get the study number and file information
            file_path = os.path.abspath(file_name)
            # we are not using file_name_info, file_name_extension, but keep it for now
            study_number, file_name_info, file_name_extension = get_study_and_remaining(file_name)
            if study_number in duplicate_study_numbers:
                if args.verbose:
                    print(f"> {study_number} ({file_name})")
                
                file_checksum = calculate_checksum(file_path)
                file_size = os.path.getsize(file_path)
                # > Get date based on file metadata
                # Ref: https://stackoverflow.com/questions/60506508/get-file-size-creation-date-and-modification-date-in-python
                # Ref: https://stackoverflow.com/questions/17958987/difference-between-python-getmtime-and-getctime-in-unix-system
                file_create_date = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getctime(file_path)))
                file_mod_date = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(os.path.getmtime(file_path)))

                # Collect metadata
                new_row = {'study_number': study_number,
                           'filename': file_name,
                           'file_path': file_path,
                           'file_name_info': file_name_info,
                           'checksum': file_checksum,
                           'filesize': file_size,
                           'file_create_date': file_create_date,
                           'file_mod_date': file_mod_date,
                           'filetype': file_name_extension,
                           'priority': ""}  # we do not prefill because it impedes prioritization and moving to _backup_duplicates-folder
                if debug:
                    print(f">>> DEBUG: file_path {file_path}")
                    print(f">>> DEBUG: file_name_info {file_name_info} <<<")
                    print(f">>> DEBUG: file_checksum {file_checksum} <<<")
                    print(f">>> DEBUG: file_size {file_size} <<<")
                    print(f">>> DEBUG: file_create_date {file_create_date} <<<")
                    print(f">>> DEBUG: file_mod_date {file_mod_date} <<<")
                    print(f">>> DEBUG: file_name_extension {file_name_extension} <<<")

                multiplicity_df = pd.concat([multiplicity_df, pd.DataFrame([new_row])], ignore_index=True)
                if debug:
                    print(f"\n>>> DEBUG: checking multiplicity meta-data <<<")
                    print(f"{multiplicity_df}")
        
    if args.verbose:
        # show contents of duplicate folder
        print(f"Contents of the [{duplicate_folder}] folder:")
        for dup_file in os.listdir(duplicate_folder):
            if dup_file.startswith(args.study_type) and args.stain in dup_file:
                print(f"  - {dup_file}")
    
    print(f'\nSaving multiplicate metadata to [{output_file_path}.metadata.csv].')
    multiplicity_df.to_csv(output_file_path, index=False)

    # Process prioritization
    print(f"\nPrioritizing multiplicate file:")
    # Determine prioritization for each study_number
    multiplicity_df = process_prioritazation(multiplicity_df, args.verbose).sort_values(by=['study_number', 'priority'], ascending=[True, False])

    print(f"\nPrioritization completed.")
    # Write the priority information to a file
    multiplicity_df.to_csv(output_file_path, index=False)
    if args.verbose:
        print(f"Written prioritization information to [{output_file_path}.metadata.csv]")

     # Move files associated with duplicate study numbers to the duplicate folder
    print(f"\nMoving files with multiplicate studynumbers to the [{duplicate_folder}] folder; redundant duplicates are moved to [{backup_duplicate_folder}].")
    for file_name in os.listdir('.'):
        if file_name in set(multiplicity_df['filename']):
            file_df = multiplicity_df.loc[multiplicity_df['filename'] == file_name].iloc[0]
            file_path = os.path.abspath(file_name)

            # Move the file to the duplicate folder
            duplicate_file = move_to_duplicates(file_path, duplicate_folder, file_df['priority'] != "", args.dry_run, args.verbose)
            if args.verbose and not args.dry_run:
                print(f"  {file_path} > {duplicate_file} ({file_df['study_number']} - {file_df['file_name_info']}))")

    # Calculate the elapsed time in seconds
    elapsed_time = time.time() - start_time
    # Convert seconds to a timedelta object
    time_delta = timedelta(seconds=elapsed_time)
    # Extract hours, minutes, seconds, and milliseconds
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = round(time_delta.microseconds / 1000)
    # Print the script execution time in the desired format
    formatted_time = f"{hours} hours, {minutes} minutes, {seconds} seconds, {milliseconds} milliseconds"

    # Write the statistics to a log file
    try:
        with open(log_file_path, 'w') as log_file:
            log_file.write(f"+ {VERSION_NAME} v{VERSION} +")
            log_file.write(f"\nIdentied and moved multiplicate image files based on specified criteria for:\n> study_type: {args.study_type}\n> stain: {args.stain}\n")
            log_file.write(f"\nTotal unique samples for stain {args.stain}: {remaining_unique_samples} | {unique_samples}\n")
            log_file.write(f"Total multiplicity files found: {sum(study_numbers_count.values())}\n")
            log_file.write(f"Total unique multiplicity files found: {len(study_numbers_count)}. Including:\n")
            for multiplicity, count in study_numbers_count.items():
                log_file.write(f"> {multiplicity}: {count}\n")

            log_file.write(f"\nScript total execution time was {formatted_time} ({time.time() - start_time:.2f} seconds).\n")
            log_file.write(f"\n+ {VERSION_NAME} v{VERSION}. {COPYRIGHT} +")
            log_file.write(f"\n{COPYRIGHT_TEXT}")

            # Print the statistics to the terminal
            if args.verbose:
                print(f"Total unique samples for stain {args.stain}: {remaining_unique_samples} | {unique_samples}")
                print(f"Total multiplicity files found: {sum(study_numbers_count.values())}")
                print(f"Total unique multiplicity files found: {len(study_numbers_count)}")

    except Exception as e:
        print(f"Error: For some reason I couldn't write to the log file: {e}.")

    print(f"\nLog written to [{log_file_path}]. Script total execution time was {formatted_time} (minus writing time).")

# Run the main function    
if __name__ == '__main__':
    main()

# Print the version number
print(f"\n+ {VERSION_NAME} v{VERSION}. {COPYRIGHT} +")
print(f"\n{COPYRIGHT_TEXT}")
# End of file
