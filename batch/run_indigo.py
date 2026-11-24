# While finding a sub-folder in [incoming] folder, take the first (alpha order),
# cd folder, run indigo on all the igs files (alpha order).
# rm folder.
# If a folder has been already been processed and no new folder is found, then shutdown the computer.

import os
import sys
import shutil
import argparse
import time
import json
import xml.etree.ElementTree as ElementTree
import datetime
import logging
import subprocess
import tarfile

str_format = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(stream=sys.stdout, format=str_format, level=logging.INFO)
logger = logging.getLogger()
logHandler = logging.FileHandler(f"log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
logHandler.setFormatter(logging.Formatter(str_format))
logger.addHandler(logHandler)

def igs_file(filename):
    if filename.endswith(".igs"):
        return True
    else:
        return False

def removeAbsolutePath(node):
    """
    Recursively traverse the given node and its children.
    If an element of tag "path" is found, its text is modified to replace
    absolute path by a relative one.
    """
    for item in node:
        if (item.tag=="path"):
            str = item.text.replace("\\", "/")
            if str.rfind("/")>-1:
                item.text = "."+str[str.rfind("/", 0, str.rfind("/")):len(str)]
        removeAbsolutePath(item)

def log(str):
    logger.info(str)
    print(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {str}")

################# MAIN ##########################

parser = argparse.ArgumentParser(description="Process all sub-folders contained in 'incoming' folder with indigo. Sub-folders must contain .igs files. Loop until no sub-folder left in 'incoming' folder.")
parser.add_argument("root_folder", type=str, help="Root folder containing 'incoming' folder and conf.json which is the conf file for indigo.")
args = parser.parse_args()

root_folder = args.root_folder
conf_file = os.path.join(root_folder, "conf.json")

conf = {}

if not os.path.exists(conf_file):
    print(f"Configuration file needed: {conf_file}")
    print("Exemple: {")
    print("\"indigo\": \"C:/programs/indigoRT/indigo_console.exe\",")
    print("\"png_folder\": \"C:/Documents/png\",")
    print("\"image_save_period\": 300,")
    print("\"halt\": 10000,")
    print("\"haltspp\": 500")
    print("}")
    sys.exit(1)
else :
    with open("conf.json") as f:
        conf = json.load(f)

incoming_folder = os.path.join(root_folder, "incoming")

while True:

    processed_folder_count = 0

    while True:

        log(f"Looking for tar files in {incoming_folder}")
        # Untar all files in incoming folder
        for file in os.listdir(incoming_folder):
            if file.endswith(".tar"):
                log(f"Untarring {file}")
                with tarfile.open(os.path.join(incoming_folder, file)) as tar:
                    tar.extractall(path=incoming_folder)
                os.remove(os.path.join(incoming_folder, file))

        log(f"Getting folders in {incoming_folder}")
        # Get list of folder to process
        folder_list = list(filter(os.path.isdir, [f"{incoming_folder}/{str}" for str in os.listdir(incoming_folder)]))

        if not folder_list:
            log("No folder to process.")
            if processed_folder_count>0:
                log("No new folder to process. Shutting down computer.")
                subprocess.run("shutdown /s /f", shell=True)
            break

        # Sort alpha order
        folder_list.sort()
        # Get first
        folder = folder_list[0]
        log(f"Changing current working dir to: {folder}")
        os.chdir(folder)

        # Get list of igs files
        igs_list = list(filter(igs_file, os.listdir('.')))
        igs_list.sort()
        log(f"List of files to process: {igs_list}")
        for igs in igs_list:
            log(f"Remove absolute paths in {igs}")
            tree = ElementTree.parse(igs)
            treeRoot = tree.getroot()
            removeAbsolutePath(treeRoot)
            # Reset width and height to 2500
            rendererSettings = treeRoot.find("renderer_settings")
            width = rendererSettings.find("width")
            width.text = "2500"
            height = rendererSettings.find("height")
            height.text = "2500"

            # Write tree to file
            tree.write(igs, encoding='utf-8', xml_declaration=True)

            igs_split = os.path.splitext(igs)
            exe = f"{conf['indigo']} \"{igs}\" -o \"{conf['png_folder']}/{igs_split[0]}.png\" -image_save_period {conf['image_save_period']} -halt {conf['halt']} -haltspp {conf['haltspp']}"
            log(exe)
            subprocess.run(exe, shell=True)
            #time.sleep(100)

        os.chdir(incoming_folder)

        # Deleting folder when done.
        log(f"Deleting {folder}")
        shutil.rmtree(folder)
        processed_folder_count += 1

    time.sleep(900) # Wait for 15 min
