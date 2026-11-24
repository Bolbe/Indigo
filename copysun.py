import sys
import xml.etree.ElementTree as ElementTree

sunFilename = sys.argv[1]
filename = sys.argv[2]

sunTree = ElementTree.parse(sunFilename+".igs")
sunRoot = sunTree.getroot()
sunSettings = sunRoot.find("background_settings")

tree = ElementTree.parse(filename+".igs")
treeRoot = tree.getroot()
rendererSettings = treeRoot.find("renderer_settings")
alpha = rendererSettings.find("render_foreground_alpha")
alpha.text = "false"
bgSettings = treeRoot.find("background_settings")
treeRoot.remove(bgSettings)
treeRoot.insert(3, sunSettings)

tree.write(filename+"_"+sunFilename+".igs", encoding='utf-8', xml_declaration=True)
