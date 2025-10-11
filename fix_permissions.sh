#!/bin/bash

# Fix permissions for Passenger deployment on cPanel
# Run this script after uploading your files to the server

echo "Fixing file permissions for Passenger deployment..."

# Set directory permissions (755 = rwxr-xr-x)
chmod 755 ~/repositories/Registeration-Bot

# Set file permissions (644 = rw-r--r--)
cd ~/repositories/Registeration-Bot
chmod 644 *.py
chmod 644 *.json
chmod 644 *.txt
chmod 644 *.md
chmod 644 *.sh

# Make scripts executable (755 = rwxr-xr-x)
chmod 755 passenger_wsgi.py
chmod 755 setup.sh
chmod 755 run.py
chmod 755 fix_permissions.sh

# Fix subdirectories
if [ -d "models" ]; then
    chmod 755 models
    chmod 644 models/*.py
fi

if [ -d "__pycache__" ]; then
    chmod 755 __pycache__
    chmod 644 __pycache__/*.pyc
fi

if [ -d "models/__pycache__" ]; then
    chmod 755 models/__pycache__
    chmod 644 models/__pycache__/*.pyc
fi

echo "Permissions fixed successfully!"
echo ""
echo "File permissions set to:"
echo "  - Directories: 755 (rwxr-xr-x)"
echo "  - Regular files: 644 (rw-r--r--)"
echo "  - Executable files: 755 (rwxr-xr-x)"
