# Replace Background settings and remove lights (spheres)

import sys
import xml.etree.ElementTree as ElementTree
import os

def processPath(node):
    for item in node:
        if (item.tag=="path"):
            str = item.text.replace("\\", "/")
            item.text = "."+str[str.rfind("/", 0, str.rfind("/")):len(str)]
        processPath(item)

def replaceCam(camFile, targetFile, suffix):
    camTree = ElementTree.parse(camFile)
    camRoot = camTree.getroot()
    camera1 = camRoot.find("camera")

    tree = ElementTree.parse(targetFile)
    treeRoot = tree.getroot()
    camera2 = treeRoot.find("camera")
    treeRoot.remove(camera2)
    treeRoot.insert(2, camera1)
    targetName = f"{os.path.splitext(targetFile)[0]}_{suffix}.igs"
    print(f"Take camera in {camFile}, put it in {targetFile}, and write the result to {targetName}.")
    tree.write(targetName, encoding='utf-8', xml_declaration=True)

# folder to process, if folder name is 2290, inside must sit a file named 2290.igs which is with sun light
foldername = sys.argv[1]
# Default Render alpha for ambiant: true or false
renderAlpha = sys.argv[2]

print(f"Processing folder {foldername}...")

bgTree = ElementTree.parse("ambiant.igs")
bgRoot = bgTree.getroot()
bgSettings = bgRoot.find("background_settings")

refFile = f"./{foldername}/{foldername}.igs"
tree = ElementTree.parse(refFile)
treeRoot = tree.getroot()

# Render alpha ?
print(f"Setting render alpha to {renderAlpha} for ambiant igs file.")
rendererSettings = treeRoot.find("renderer_settings")
alpha = rendererSettings.find("render_foreground_alpha")
alpha.text = renderAlpha

# Replace bg ambiant settings
print(f"Replacing light by ambiant light.")
settings = treeRoot.find("background_settings")
treeRoot.remove(settings)
treeRoot.insert(3, bgSettings)

# Remove spot lights (spheres)
print(f"Removing spot lights.")
for item in treeRoot:
    if (item.tag=="sphere"):
        treeRoot.remove(item)

ambiantFile = f"./{foldername}/{foldername}a.igs"
print(f"Writing ambiant file to {ambiantFile}.")
tree.write(ambiantFile, encoding='utf-8', xml_declaration=True)

# Create files for each cam
camCount = 1
for camfile in os.listdir(f"./{foldername}/cams"):
    abscam = f"./{foldername}/cams/{camfile}"
    if camfile.endswith(".igs"):
        camCount = camCount+1
        replaceCam(abscam, refFile, camCount)
        replaceCam(abscam, ambiantFile, camCount)


# In the end, replace absolute path by relative paths            
for filename in os.listdir(f"./{foldername}"):
    fullname = f"./{foldername}/{filename}"
    if filename.endswith(".igs"):
        print(f"Removing absolute path in {fullname}.")
        tree = ElementTree.parse(fullname)
        treeRoot = tree.getroot()
        processPath(treeRoot)
        tree.write(fullname, encoding='utf-8', xml_declaration=True)
