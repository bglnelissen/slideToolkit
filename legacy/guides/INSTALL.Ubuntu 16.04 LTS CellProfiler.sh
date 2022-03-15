#!/bin/bash
# install CellProfiler on Ubuntu 16.04 LTS
# tested in VirtualBox for Ubuntu and Lubuntu 16.04

# B. Nelissen
# update apt-get
sudo apt-get update && sudo apt-get upgrade

# update pip
pip install --upgrade pip

# java
sudo apt-get --yes install default-jre

# Install packages
sudo apt-get --yes install cython git libmysqlclient-dev libhdf5-dev libxml2-dev libxslt1-dev openjdk-8-jdk python-dev python-pip python-h5py python-matplotlib python-mysqldb  python-scipy python-vigra python-wxgtk3.0 python-zmq

# CellProfiler in /opt
sudo git clone https://github.com/CellProfiler/CellProfiler.git $HOME/git/CellProfiler
cd $HOME/git/CellProfiler

# Checkout the latest stabel version
git checkout stable

# Compile / install python dependencies using non root rights.
sudo chmod -R o+w /usr/local/lib/python2.7/dist-packages /usr/local/bin
cd $HOME/git/CellProfiler
# pip install --editable . # ERROR WHEN INSTALLING WITHOUT SUDO RIGHTS.
sudo pip install --editable .
# revoke permissions
sudo chmod -R o-w /usr/local/lib/python2.7/dist-packages /usr/local/bin

# Check installation using 
echo
echo "To let you know, this installation used 'sudo' rights for the pip installs. This is a quick and dirty way to fix some errors during install but is also the wrong way for the long term. It should have no consequences for normal use of CellProfiler."
echo
command -v cellprofiler

# How to delete:
# rm -rf /usr/local/bin/cellprofiler
# rm -rf $HOME/git/CellProfiler
# rm -rf /usr/lib/python2.7/dist-packages/*