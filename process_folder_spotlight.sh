#!/bin/bash
echo "Preparing folder: $1"
python3 process_folder_spotlight.py $1
python3 remove_abs_path.py $1