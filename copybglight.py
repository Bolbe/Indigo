# Replace Background settings and remove lights (spheres)

import sys
import xml.etree.ElementTree as ElementTree

# igs file with background settings
bgFilename = sys.argv[1]
# igs target file
filename = sys.argv[2]
# Render alpha: true or false
renderAlpha = sys.argv[3]

bgTree = ElementTree.parse(bgFilename+".igs")
bgRoot = bgTree.getroot()
bgSettings = bgRoot.find("background_settings")

tree = ElementTree.parse(filename+".igs")
treeRoot = tree.getroot()

# Render alpha ?
rendererSettings = treeRoot.find("renderer_settings")
alpha = rendererSettings.find("render_foreground_alpha")
alpha.text = renderAlpha

# Replace bg settings
settings = treeRoot.find("background_settings")
treeRoot.remove(settings)
treeRoot.insert(3, bgSettings)

# Remove lights (spheres)
for item in treeRoot:
    if (item.tag=="sphere"):
        treeRoot.remove(item)

tree.write(filename+"_"+bgFilename+".igs", encoding='utf-8', xml_declaration=True)
