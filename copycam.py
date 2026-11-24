import sys
import xml.etree.ElementTree as ElementTree

camFilename = sys.argv[1]
filename = sys.argv[2]

camTree = ElementTree.parse(camFilename+".igs")
camRoot = camTree.getroot()
camera1 = camRoot.find("camera")

tree = ElementTree.parse(filename+".igs")
treeRoot = tree.getroot()
camera2 = treeRoot.find("camera")
treeRoot.remove(camera2)
treeRoot.insert(2, camera1)

tree.write(filename+"_"+camFilename+".igs", encoding='utf-8', xml_declaration=True)
