import sys
import xml.etree.ElementTree as ElementTree
import os

foldername = sys.argv[1]

def processPath(node):
    for item in node:
        if (item.tag=="path"):
            str = item.text.replace("\\", "/")
            if str.rfind("/")>-1:
                item.text = "."+str[str.rfind("/", 0, str.rfind("/")):len(str)]
        processPath(item)
            
for filename in os.listdir(f"./{foldername}"):
    fullname = f"./{foldername}/{filename}"
    if filename.endswith(".igs"):
        print(f"Removing absolute path in {fullname}.")
        tree = ElementTree.parse(fullname)
        treeRoot = tree.getroot()
        processPath(treeRoot)
        # Reset width and height to 2500
        rendererSettings = treeRoot.find("renderer_settings")
        width = rendererSettings.find("width")
        width.text = "2500"
        height = rendererSettings.find("height")
        height.text = "2500"
        tree.write(fullname, encoding='utf-8', xml_declaration=True)
