#!/usr/bin/env python3

"""
    slideLookup
    This script is designed to perform a whole-slide image (WSI) sample lookup (--samples) in a directory or 
    a set of directories (--dir) containing WSI. By default, the script will look for the following 
    directories: {DEFAULT_DIRECTORIES}. These can be changed with the `--dir` flag.

    Optionally, the found files can be copied (--copy) to another directory (--copy-dir). It provides extra 
    information (--verbose) if requested.

    The script is executed using `python slideLookup.py` from the command line. Users can provide sample codes
    and directories as arguments. Optionally, they can specify whether to copy the found files and provide a
    directory for copying. Extra information can be printed with the `--verbose` flag.

    Example usage:
    python slideLookup.py --samples AE4211 AE3422  --dir CD14 CD3 [options: --copy --copy-dir /home/user/Desktop/ --verbose]

    Options:
    --samples, -s       List of sample codes to look for in filenames. Required.
    --dir, -d           List of directories to search for the samples. Required.
    --study_type, -t    Specify the study type prefix, e.g., AE. Required.
    --log, -l           Specify the log-filename which will be of the form [`study_type`.slideLookup.`log`]. Required.
    --copy, -c          Copy the found files. Optional.
    --copy_dir, -cd     Set directory to copy the found files. Optional.
    --verbose, -v       Print extra information. Optional.
    --version, -V       Print version. Optional.
    --help, -h          Print help message. Optional.

    """

# Version information
VERSION_NAME = 'slideLookup'
VERSION = '1.0.0'
VERSION_DATE = '2023-01-05'
COPYRIGHT = 'Copyright 1979-2023. Sander W. van der Laan | s.w.vanderlaan [at] gmail [dot] com | https://vanderlaanand.science.'
COPYRIGHT_TEXT = f'\nThe MIT License (MIT). \n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and \nassociated documentation files (the "Software"), to deal in the Software without restriction, \nincluding without limitation the rights to use, copy, modify, merge, publish, distribute, \nsublicense, and/or sell copies of the Software, and to permit persons to whom the Software is \nfurnished to do so, subject to the following conditions: \n\nThe above copyright notice and this permission notice shall be included in all copies \nor substantial portions of the Software. \n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, \nINCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR \nPURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS \nBE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, \nTORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE \nOR OTHER DEALINGS IN THE SOFTWARE. \n\nReference: http://opensource.org.'

# Import required packages
import os
import argparse
from argparse import RawTextHelpFormatter
import shutil
import time
from datetime import datetime
from datetime import timedelta

# Define default directories
DEFAULT_DIRECTORIES = ["CD14", "CD3", "CD31", "CD34", "CD3_CD56_NKT", "CD42B", "CD66b", "CD68", "CD8",
                       "CD86", "EVG", "FIBRIN", "GLYCC", "HE", "HE-FIBRIN", "HHIPL1", "MPO", "MT", "SMA",
                       "SR", "SR_POLARIZED", "VONWILLEBRANDFACTOR"]

### WANT TO ADD THIS LATER ###
### a more secure way to do this is to use the os.path.join() function
DEFAULT_COPY_DIRECTORY = "/hpc/dhl_ec/VirtualSlides/Projects/histo_lookups"
DEFAULT_AE_VIRTUALSLIDES = "/data/isi/d/dhl/ec/VirtualSlides/AE-SLIDES"
DEFAULT_AAA_VIRTUALSLIDES = "/data/isi/d/dhl/ec/VirtualSlides/AAA-SLIDES"

def get_lookup_directory(study_type, verbose):
    if study_type == 'AE':
        return DEFAULT_AE_VIRTUALSLIDES
        ### LOCAL TESTING ###
        ### return '/Users/USERNAME/SOMEDIRECTORY'
    elif study_type == 'AAA':
        return DEFAULT_AAA_VIRTUALSLIDES
    else:
        raise ValueError(f"Invalid study type: {study_type}. Supported types are 'AE' and 'AAA'.")

# Define function to find samples in directories
def find_samples_in_directories(samples, study_type, directories, verbose, copy_dir):
    lookup_directory = get_lookup_directory(study_type, verbose)
    if verbose:
        print(f"Looking for {study_type} slides in: [ {lookup_directory} ]")

    # Loop over the directories    
    for directory in directories:
        lookup_directory_walk = os.path.join(lookup_directory, directory)
        if verbose:
            print(f"> checking contents of directory {directory} ({lookup_directory_walk})...")
        
        # Loop over the subdirectories
        for root, dirs, files in os.walk(lookup_directory_walk):

            # Loop over the files
            for file in files:

                # Loop over the samples
                for sample in samples:

                    # Check if the sample is in the file
                    if sample in file:
                        if verbose:
                            print(f"Found {sample} in {directory} as {file}.")
                        
                        # Copy the file to the copy directory
                        if copy_dir:
                            create_copy_directory(copy_dir, verbose)
                            copy_file_to_directory(os.path.join(root, file), copy_dir, verbose)
                            if verbose:
                                print(f"...copying...")

# Define function to create directory to copy files to
def create_copy_directory(copy_dir, verbose):
    if not os.path.exists(copy_dir):
        os.makedirs(copy_dir, exist_ok=True)
        if verbose:
            print(f"> Created copy directory: {copy_dir}.")
    else:
        if verbose:
            print(f"> Copy directory already exists: {copy_dir}.")
            list_folder_content(copy_dir)
# Define function to copy files to directory
def copy_file_to_directory(file_path, copy_dir, verbose):
    shutil.copy(file_path, copy_dir)
    if verbose:
        print(f"> Copied {file_path} to {copy_dir}.")

def list_folder_content(folder_path):
    try:
        # List the content of the folder
        content = os.listdir(folder_path)

        # Print the content
        print(f"Content of '{folder_path}':")
        for item in content:
            print(item)

    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to access folder '{folder_path}'.")

# Define main function
def main():
    parser = argparse.ArgumentParser(description=f'''
+ {VERSION_NAME} v{VERSION} +

This script is designed to perform a whole-slide image (WSI) sample lookup (--samples) in a directory or 
a set of directories (--dir) containing WSI. By default, the script will look for the following 
directories: [ {DEFAULT_DIRECTORIES} ]. These can be changed with the `--dir` flag. By default a log file
is written to the current working directory; this is changed by providing --copy_dir . The `--log` flag 

Optionally, the found files can be copied (--copy) to another directory (--copy-dir). By default, the
files will be copied to the following directory: [ {DEFAULT_COPY_DIRECTORY} ]. It provides extra information 
(--verbose) if requested.

Example usage:
python slideLookup.py --samples AE4211 AE3422  --dir CD14 CD3 [options: --copy --copy-dir /home/user/Desktop/ --verbose]
        ''',
        epilog=f'''
+ {VERSION_NAME} v{VERSION}. {COPYRIGHT} \n{COPYRIGHT_TEXT}+''', 
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--samples', '-s', nargs='+', required=True, help='List of whole-slide image (WSI) samples, e.g. AE4211, AE3422. Required.')
    parser.add_argument('--dir', '-d', nargs='+', help='List of directories, e.g. CD14 CD3. Required.', default=DEFAULT_DIRECTORIES)
    parser.add_argument('--study_type', '-t', required=True, help='Specify the study type prefix, e.g., AE. Required.')
    parser.add_argument('--log', '-l', help='Specify the log-filename which will be of the form [`todays_date`.`study_type`.slideLookup.`log`.log]. Optional.', default="AWESOMEPROJECT")
    parser.add_argument('--copy', '-c', action='store_true', help='Copy files to copy-dir. Optional.')
    parser.add_argument('--copy_dir', '-cd', help='Directory to copy files. Optional.')
    ### WANT TO ADD THIS LATER ###
    ### parser.add_argument('--force', '-f', help='Overwrite files if they are already copied. Optional.')
    parser.add_argument('--verbose', '-v', action='store_true', help='Print extra information. Optional.')
    parser.add_argument('--version', '-V', action='version', version=f'%(prog)s {VERSION} ({VERSION_DATE}).')
    args = parser.parse_args()

    # Start the timer
    start_time = time.time()
    
    # Get today's date
    today_date = datetime.now()

    # Format the date as yyyymmdd
    formatted_today = today_date.strftime("%Y%m%d")

    # Start the script
    print(f"+ {VERSION_NAME} v{VERSION} ({VERSION_DATE}) +")
    print(f"\nLookup WSI files in VirtuaSlides of the Athero-Express and AAA-Express Biobank Studies.")
    if args.verbose:
        print(f"\nLooking up using the following conditions:")
        print(f"> Study type: {args.study_type}")
        print(f"> Direcor(y/ies): {args.dir}")
        print(f"> Samples: {args.samples}")
    
    # Set how we handle the copy directory
    if args.copy:
        if args.copy_dir:
            COPY_DIRECTORY = args.copy_dir
            log_folder = os.path.join(COPY_DIRECTORY)
            print(f"\nNotice: You set to copy WSI files and specified a directory to copy the files to; setting it to ({COPY_DIRECTORY}).")
        else:
            COPY_DIRECTORY = DEFAULT_COPY_DIRECTORY
            ### LOCAL TESTING ###
            ### COPY_DIRECTORY = "/Users/USERNAME/SOMEDIRECTORY"
            log_folder = os.path.join(COPY_DIRECTORY)
            print(f"\nNotice: You set to copy WSI files, but did not specify a directory to copy the files to; setting it to default ({COPY_DIRECTORY}).")
    else:
        COPY_DIRECTORY = None
        log_folder = os.getcwd()
        print(f"\nNotice: You did not specify the copy argument. So we are only performing the lookup without copying.")
        if args.verbose:
            print(f">>> Directory was not set ({COPY_DIRECTORY}) <<<\n")

    # Set the log file path
    log_file_path = os.path.join(log_folder, formatted_today + '.' + args.study_type + '.slideLookup.' + args.log + '.log')

    # Find the samples in the directories
    print(f"\nLooking for the given samples.\n")
    find_samples_in_directories(args.samples, args.study_type, args.dir, args.verbose, COPY_DIRECTORY)

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
            log_file.write(f"\nLookup WSI files in VirtuaSlides of the Athero-Express and AAA-Express Biobank Studies.\n")
            log_file.write(f"\nExecuted lookup using the following conditions:")
            log_file.write(f"\n> Study type: {args.study_type}")
            log_file.write(f"\n> Direcor(y/ies): {args.dir}")
            log_file.write(f"\n> Samples: {args.samples}\n")

            ### WANT TO ADD THIS LATER ###
            # log_file.write(f"\nFound the following samples:.\n")
            # log_file.write(f" > sample - directory - filename") # {sample} - {directory} - {file}
            # log_file.write(f"Total WSI samples found: X .\n") # {sum(study_numbers_count.values())}
            # log_file.write(f"Total WSI samples search for: Y .\n") # {len(study_numbers_count)}
            # log_file.write(f"Total WSI samples not found: Z .\n") # {len(study_numbers_count) - sum(study_numbers_count.values())}
            
            log_file.write(f"\nScript executed on {today_date.strftime('%Y-%m-%d')}. Total execution time was {formatted_time} ({time.time() - start_time:.2f} seconds).\n")
            log_file.write(f"\n+ {VERSION_NAME} v{VERSION}. {COPYRIGHT} +")
            log_file.write(f"\n{COPYRIGHT_TEXT}")

            ### WANT TO ADD THIS LATER ###
            # Print the statistics to the terminal
            # if args.verbose:
            #     print(f"Total WSI samples found: X .\n") # {sum(study_numbers_count.values())}
            #     print(f"Total WSI samples search for: Y .\n") # {len(study_numbers_count)}
            #     print(f"Total WSI samples not found: Z .\n") # {len(study_numbers_count) - sum(study_numbers_count.values())}
        print(f"\nLog written to [{log_file_path}].")

    except Exception as e:
        print(f"\nError: For some reason I couldn't write to the log file: {e}. Log was not written. ")

    print(f"\nScript executed on {today_date.strftime('%Y-%m-%d')}. Total execution time was {formatted_time} (minus writing time).")

if __name__ == "__main__":
    main()

# Print the version number
print(f"\n+ {VERSION_NAME} v{VERSION} ({VERSION_DATE}). {COPYRIGHT} +")
print(f"{COPYRIGHT_TEXT}")
# End of file
