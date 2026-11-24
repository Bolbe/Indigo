import xml.etree.ElementTree as ElementTree
import os

def replaceCam(camFile, sourceFile, targetFile):
    camTree = ElementTree.parse(camFile)
    camRoot = camTree.getroot()
    camera1 = camRoot.find("camera")

    tree = ElementTree.parse(sourceFile)
    treeRoot = tree.getroot()
    camera2 = treeRoot.find("camera")
    treeRoot.remove(camera2)
    treeRoot.insert(2, camera1)
    print(f"Take camera in {camFile}, put it in {sourceFile}, and write the result to {targetFile}.")
    tree.write(targetFile, encoding='utf-8', xml_declaration=True)
    