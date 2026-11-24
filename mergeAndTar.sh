#!/bin/bash

# After saving scene for each cameras, merge the meshe file. Turn this:

# -rwx------@   1 bolbe  staff  1301836 Mar 19 21:11 6077.igs
# -rw-r--r--@   1 bolbe  staff   650195 Mar 19 21:14 6077_1_ambient.igs
# drwxr-x---@ 495 bolbe  staff    15840 Mar 19 21:14 6077_1_ambient_meshes
# -rw-r--r--@   1 bolbe  staff   650181 Mar 19 21:18 6077_2_ambient.igs
# drwxr-x---@ 495 bolbe  staff    15840 Mar 19 21:17 6077_2_ambient_meshes
# -rw-r--r--@   1 bolbe  staff   650166 Mar 19 21:22 6077_3_ambient.igs
# drwxr-x---@ 495 bolbe  staff    15840 Mar 19 21:22 6077_3_ambient_meshes
# -rw-r--r--@   1 bolbe  staff   650181 Mar 19 21:25 6077_4_ambient.igs
# drwxr-x---@ 495 bolbe  staff    15840 Mar 19 21:25 6077_4_ambient_meshes
# -rw-r--r--@   1 bolbe  staff   650185 Mar 19 21:28 6077_5_ambient.igs
# drwxr-x---@ 495 bolbe  staff    15840 Mar 19 21:28 6077_5_ambient_meshes
# drwx------  377 bolbe  staff    12064 Mar 19 20:40 6077_Images
# drwx------  495 bolbe  staff    15840 Mar 19 19:17 6077_meshes
# drwx------@   4 bolbe  staff      128 Mar 19 21:11 ambient_Images
# drwx------    7 bolbe  staff      224 Mar 19 20:40 cams

# into this:

# -rwx------@   1 bolbe  staff  1301836 Mar 19 22:14 6077.igs
# -rw-r--r--@   1 bolbe  staff   645265 Mar 19 22:14 6077_1_ambient.igs
# -rw-r--r--@   1 bolbe  staff   645251 Mar 19 22:14 6077_2_ambient.igs
# -rw-r--r--@   1 bolbe  staff   645236 Mar 19 22:14 6077_3_ambient.igs
# -rw-r--r--@   1 bolbe  staff   645251 Mar 19 22:14 6077_4_ambient.igs
# -rw-r--r--@   1 bolbe  staff   645255 Mar 19 22:14 6077_5_ambient.igs
# drwx------  377 bolbe  staff    12064 Mar 19 20:40 6077_Images
# drwxr-x---@ 495 bolbe  staff    15840 Mar 19 21:25 6077_meshes
# drwx------@   4 bolbe  staff      128 Mar 19 21:11 ambient_Images
# drwx------    7 bolbe  staff      224 Mar 19 20:40 cams

# Check if a folder name argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 [folder name]"
  exit 1
fi

# Call the Python script to merge meshes
python3 merge_meshes.py "$1"

# Define the new sequence to replace the old sequence in the .igs files
new_sequence="$1_meshes"
cd $1
# Loop over all .igs files in the current directory
for file in *.igs; do
  # Check if there are any .igs files
  if [ -e "$file" ]; then
    # Extract the filename without the extension as the old sequence
    old_sequence="${file%.igs}_meshes"
    echo "sed -i 's/$old_sequence/$new_sequence/g' '$file'"
    # Use sed to replace the old sequence with the new sequence in each file
    sed -i "" "s/$old_sequence/$new_sequence/g" "$file"
  else
    echo "No more .igs files."
    break
  fi
done
cd ..

# Then, create a tarball of the folder eg: tar -cf 6042.tar 6042
export COPYFILE_DISABLE=1
tar --exclude='.DS_Store' --exclude='._*' -cf "$1.tar" "$1"

# Finally, remove the original folder
rm -rf "$1"