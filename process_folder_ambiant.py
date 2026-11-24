import argparse
import xml.etree.ElementTree as ElementTree
import os
import utilities

############### MAIN ########################
parser = argparse.ArgumentParser(description="Process folder as ambient light.")
parser.add_argument("foldername", type=str, help="Folder to process")
args = parser.parse_args()

print(f"Processing folder {args.foldername}...")

bgTree = ElementTree.parse("ambient.igs")
bgRoot = bgTree.getroot()
bgSettings = bgRoot.find("background_settings")

refFile = f"./{args.foldername}/{args.foldername}.igs"
tree = ElementTree.parse(refFile)
treeRoot = tree.getroot()

# Replace bg ambient settings
print(f"Replacing light by ambient light.")
settings = treeRoot.find("background_settings")
treeRoot.remove(settings)
treeRoot.insert(3, bgSettings)

# Remove spot lights (spheres) if any.
print(f"Removing spot lights.")
for item in treeRoot:
    if (item.tag=="sphere"):
        treeRoot.remove(item)

ambientFile = f"./{args.foldername}/{args.foldername}_ambient.igs"
print(f"Writing ambient file to {ambientFile}")
tree.write(ambientFile, encoding='utf-8', xml_declaration=True)

# Create files for each cam
camCount = 0
for camfile in os.listdir(f"./{args.foldername}/cams"):
    abscam = f"./{args.foldername}/cams/{camfile}"
    if camfile.endswith(".igs"):
        camCount = camCount+1
        utilities.replaceCam(abscam, ambientFile, f"./{args.foldername}/{args.foldername}_{camCount}_ambient.igs")

os.remove(ambientFile)
