import argparse
import re
import subprocess
import os

# In order to work, you need an original folder called 6076_meshes and a few folders created afterwards 
# and called 6076_1_spot_meshes, 6076_2_spot_meshes, and so on.
# This script deletes the original folder 6076_meshes, then renames the 6076_1_spot_meshes (or 6076_1_ambiant_meshes) to 6076_meshes and delete the remaining folders.

parser = argparse.ArgumentParser(description="Merge mesh files in folder.")
parser.add_argument("foldername", type=str, help="Folder to process")
args = parser.parse_args()

print(f"Processing folder {args.foldername}...")

# Define the regular expression matching {args.foldername}_(anything)_meshes where (anything) is a non-empty string (e.g. spot or ambiant)
regex = f"{args.foldername}_.+_meshes"

# Stop here if not foler matching the regex can be found
found = False
for folder in os.listdir(f"{args.foldername}"):
    if re.match(regex, folder):
        found = True
        break
if not found:
    print(f"No folder matching {regex} found in {args.foldername}.")
    exit(1)

# Erase original folder
print(f"Deleting original folder ./{args.foldername}/{args.foldername}_meshes")
subprocess.run(["rm", "-rf", f"{args.foldername}/{args.foldername}_meshes"])

# Find first folder matching the regex and rename it to {args.foldername}_meshes, delete all other folders matching the regex
print(f"Renaming first folder matching {regex} to {args.foldername}_meshes")
for folder in os.listdir(f"{args.foldername}"):
    if re.match(regex, folder):
        subprocess.run(["mv", f"{args.foldername}/{folder}", f"{args.foldername}/{args.foldername}_meshes"])
        print(f"Renamed {folder} to {args.foldername}_meshes")
        break
for folder in os.listdir(f"{args.foldername}"):
    if re.match(regex, folder):
        subprocess.run(["rm", "-rf", f"{args.foldername}/{folder}"])
        print(f"Deleted {folder}")
