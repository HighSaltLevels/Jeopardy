#!/bin/bash

echo "Checking to see if run with root priveleges..."
if [[ $EUID -ne 0 ]]; then
    echo "Permission Denied. This installer needs to be run as root!"
    exit 1
fi

echo "Ensuring python3 and pyqt5 are installed..."
apt-get update
apt-get install python3
apt-get install python3-pyqt5

echo "Creating directory for files..."
mkdir /usr/local/lib/jeopardy

echo "Placing files where they belong..."
mv icon.jpg /usr/local/lib/jeopardy/
mv dailydouble.py /usr/lib/python3/dist-packages/
mv questionwindow.py /usr/lib/python3/dist-packages/
mv jeopardy.py /usr/local/bin/jeopardy

echo "Giving permissions for files..."
chmod +x /usr/local/bin/jeopardy

echo "Installation complete. To run the program, simply type 'jeopardy'"

