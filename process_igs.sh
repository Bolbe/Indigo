#!/bin/sh
# Replace all occurences of E:/GEB/IGS by . in the file then replace \ by /
for filename in *.igs; do
    sed 's|E:/GEB/IGS|.|' < "$filename" >"$filename.tmp1"
    rm "$filename"
    sed 's/\\/\//g' < "$filename.tmp1" >"$filename.tmp2"
    rm "$filename.tmp1"
    mv "$filename.tmp2" "$filename"
done
    