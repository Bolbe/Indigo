import os
import hashlib
import sys
import xml.etree.ElementTree as ElementTree

foldername = sys.argv[1]
path = foldername+"/"+foldername+"_Images"

# list of all files with their md5
fileMap = {}
# list of md5
md5List = []

def processPath(node):
    for item in node:
        if (item.tag=="path" and item.text.endswith(".png")):
            str = item.text.replace("\\", "/")
            name = str[str.rfind("/")+1:len(str)]
            if name in fileMap:
                item.text = str[0:str.rfind("/")]+"/"+fileMap[name]+".png"
            else:
                print(f"STOP ! Cannot find {name} in fileMap")
                exit(0)
        processPath(item)

for filename in os.listdir(path):
    if filename.endswith(".png"):
        f = open(path+"/"+filename, 'rb')
        md5 = hashlib.md5(f.read()).hexdigest()
        f.close()
        fileMap[filename] = md5
        print(f"Processing {filename} ({len(fileMap)})")
        if not md5 in md5List:
            md5List.append(md5)
            print(f"Recording new MD5: {md5} ({len(md5List)})")
            os.rename(path+"/"+filename, path+"/"+md5+".png")
        else:
            os.remove(path+"/"+filename)

print(f"{len(fileMap)} files reduced to {len(md5List)} ({len(md5List)*100/len(fileMap)}%)")

for filename in os.listdir(f"./{foldername}"):
    fullname = f"./{foldername}/{filename}"
    if filename.endswith(".igs"):
        print(f"Replacing png files path in {fullname}.")
        tree = ElementTree.parse(fullname)
        treeRoot = tree.getroot()
        processPath(treeRoot)
        tree.write(fullname, encoding='utf-8', xml_declaration=True)
