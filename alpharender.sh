#!/bin/bash
for filename in $1/*.igs; do
    python3 alpharender.py $filename $2
done