import xml.etree.ElementTree as ElementTree
import os
import argparse
import utilities

############### MAIN ########################
parser = argparse.ArgumentParser(description="Process folder as spotlight.")
parser.add_argument("foldername", type=str, help="Folder to process")
args = parser.parse_args()

print(f"Processing folder {args.foldername}...")

refFile = f"./{args.foldername}/{args.foldername}.igs"

# Create files for each cam
camCount = 0
for camfile in os.listdir(f"./{args.foldername}/cams"):
    abscam = f"./{args.foldername}/cams/{camfile}"
    if camfile.endswith(".igs"):
        camCount = camCount+1
        utilities.replaceCam(abscam, refFile, f"./{args.foldername}/{args.foldername}_{camCount}_spot.igs")

