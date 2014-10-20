#!/bin/bash
# Onetime slideToolkit install script for Ubuntu
# Do not use this script, it is build for testing purposes.
# B. Nelissen

# Check Ubuntu version
if [[ "12.04" != "$(lsb_release -r | awk '{print $2}')" ]]; then
  echo "No Ubuntu 12.04 LTS found."
  exit 1
fi

# Let's roll