#!/bin/bash

# for f in *\ *; do mv "$f" "${f// /_}"; done

# find  *.ndpi -exec /hpc/local/CentOS7/dhl_ec/software/slideToolKit/slideDirectory -f "{}" \;

find "$(pwd)" -iname "*.ndpi" -exec /hpc/local/CentOS7/dhl_ec/software/slideToolKit/slideDirectory -f "{}" \;