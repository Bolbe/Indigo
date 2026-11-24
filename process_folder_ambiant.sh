#!/bin/bash
echo "Preparing folder: $1"
cp -R ./ambient_Images $1
python3 process_folder_ambiant.py $1
python3 remove_abs_path.py $1

