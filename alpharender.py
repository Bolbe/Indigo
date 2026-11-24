import sys
import argparse
import xml.etree.ElementTree as ElementTree

parser = argparse.ArgumentParser(description="Set alpha value true or false.")
parser.add_argument("filename", type=str, help="IGS file name")
parser.add_argument("alphavalue", type=str, help="true or false")
args = parser.parse_args()

if (args.alphavalue!="true" and args.alphavalue!="false"):
    print("Alpha value must be true or false.")
    sys.exit(1)

tree = ElementTree.parse(args.filename)
treeRoot = tree.getroot()
rendererSettings = treeRoot.find("renderer_settings")
alpha = rendererSettings.find("render_foreground_alpha")
alpha.text = args.alphavalue

tree.write(args.filename, encoding='utf-8', xml_declaration=True)
