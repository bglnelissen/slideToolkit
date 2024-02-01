Instructions for SlideQuantify_V2

Call the script like:
bash slideQuantify_V2 [arg1: STAIN] [arg2: path_to_cellprofiler_pipeline] [arg3: path_to_working_directory] [arg4: path_to_procces_file] [arg5: y.name@umcutrecht.nl] [arg6: FAIL] [arg7: 2000] [arg8: 2] [args9: path/to/dir (OPTIONAL)]"
e.g:
bash slideQuantify_V2 EVG ./EVG.cp413.v1.1.cppipe ./ ./all_snr.txt t.s.peters-4@umcutrecht.nl NONE 2000 1 ./masks/
or
bash slideQuantify_V2 EVG ./EVG.cp413.v1.1.cppipe ./ ./all_snr.txt t.s.peters-4@umcutrecht.nl NONE 2000 1

Things to note:
- arg3: path_to_working_directory:
This directory should contain the folders _ndpi and/or _tif containing the images to process.
e.g:
    - _ndpi
        - AE1....
        - AE2....
        - ....
    - _tif
        - AE3....
        - AE4....
        - ....

- arg4: path_to_procces_file:
This should be a .txt file containing a list of all study numbers to process.
e.g:
study_numbers.txt
    AE1
    AE2
    AE3
    AE4
    ....

- arg9:
This is an optinal parameter. If used it should point to a directory containing the masks for the images you want to process.
If left empty, masks will be created using EntropyMasker