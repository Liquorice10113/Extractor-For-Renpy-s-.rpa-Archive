import os
import zlib
import pickle

from sys import argv

def indexArchive(fileName):
    """
    Load the index of the archive file. OWO
    """
    
    file = open(fileName, "rb")
    lines = file.readline()

    # 3.0 Branch
    if lines.startswith(b"RPA-3.0 "):
        offset = int(lines[8:24], 16)
        key = int(lines[25:33], 16)
        file.seek(offset)
        index = pickle.loads(zlib.decompress(file.read()))
        for item in index.keys():
            index[item] = (index[item][0][0] ^ key, index[item][0][1] ^ key)
        file.close()

    # 2.0 Branch
    if lines.startswith(b"RPA-2.0 "):
        offset = int(lines[8:], 16)
        file.seek(offset)
        index = pickle.loads(zlib.decompress(file.read()))
        file.close()
    
    return index

def writeSeparateFile(fileName,targetFileName,offset,size):
    """
    Read and write. OWO
    """
    chunkSize = 20971520
    file = open(fileName,"rb")
    targetFile = open(targetFileName,"wb")
    
    file.seek(offset)
    while size >chunkSize:
        size -= chunkSize
        targetFile.write(file.read(chunkSize))
    targetFile.write(file.read(size))
    
    file.close()
    targetFile.close()

if __name__ == "__main__":
    try:
       fileName = argv[1].replace("\"","")
    except:
        fileName = input("输入文件完整路径>>>").replace("\"","")
    if "\\" in fileName:
        root = fileName.replace(".rpa","") + "/"
    else:
        root = fileName.replace(".rpa","") + "/"
    index = indexArchive(fileName)
    
    for targetFileName, location in index.items():
        print(targetFileName)
        offset,size = location
        path = "/".join(targetFileName.split("/")[:-1])
        if not os.path.exists(root+path):
            os.makedirs(root+path)
        writeSeparateFile(fileName,root+targetFileName,offset,size)
