#
# tested on python 3.6
#
# !WARNING! Saves files into your current dir. Make sure you have enough Diskspace
# !WARNING! Cheap hacks used. Do not use this in Production!

from ftplib import FTP
from hashlib import md5
from io import BytesIO
from multiprocessing import Process
import os
import gzip

mainURL = 'ftp.ncbi.nlm.nih.gov'
pSIZES = 50

def info(pString):
    print("-------------------")
    print(pString)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())
    print('\n')


def getHashsData(newFileName, urlDir):
    ftp = FTP(mainURL)
    ftp.login()
    ftp.cwd(urlDir)
    ftpFiles = ftp.nlst()
    pubmedmd5s = {}
    tmpFBytes = BytesIO()

    info("download from Dir started: " + urlDir)

    for fName in ftpFiles:
        if ".xml.gz.md5" in fName:
            ftp.retrbinary('RETR %s' % fName, tmpFBytes.write)
            tmpLine = tmpFBytes.getvalue().decode("UTF-8")
            pubmedmd5s[fName[0:21]] = tmpLine[28:60]  #cheap hack
            tmpFBytes.seek(0)
            tmpFBytes.truncate(0)

    # writing all files with md5hash we need to download into a txt
    downloadFiles = open(newFileName,'w')
    for key, val in pubmedmd5s.items():
        downloadFiles.write(key + "=" + val + "\n")

    downloadFiles.write
    downloadFiles.close()

    ftp.quit()
    info("finished downloading")

def getHashs():
    info("Program Started")
    proOne = Process(target=getHashsData, args=("downloadFileBaseline.txt", "pubmed/baseline/",))
    proTwo = Process(target=getHashsData, args=("downloadFilesUpdate-16-11-17.txt", "pubmed/updatefiles/",))
    proOne.start()
    proTwo.start()

    info("both processes Started")
    proOne.join()
    proTwo.join()


def getfileData( urlDir, file_mData ):
    fmData = file_mData
    ftp = FTP(mainURL)
    ftp.login()
    ftp.cwd(urlDir)

    tmpFBytes = BytesIO()

    for fName, md5sum in fmData.items():
        ftp.retrbinary('RETR %s' % fName, tmpFBytes.write)
        md5sumCalc = md5(tmpFBytes.getbuffer())
        if(md5sumCalc.hexdigest() == md5sum):
            filebin = gzip.decompress(tmpFBytes.getvalue())
            with open(fName[0:18], 'wb') as finalfile:        # WARNING CHEAP HACK HERE
                finalfile.write(filebin)
                finalfile.write
        tmpFBytes.seek(0)
        tmpFBytes.truncate(0)

    ftp.close()


def getfileNames( urlDir, fileListTXT ):

    with open(fileListTXT, 'r') as f:

        mullines = f.readlines()
        procss = []
        i = 0
        file_mData = {}     # filename + MD5 hash
        for line in mullines:
            file_mData[line[0:21]] = line[22:54]
            i += 1
            if i > pSIZES:
                proc = Process(target=getfileData, args=(urlDir, file_mData,))
                procss.append(proc)
                proc.start()
                i = 0
                file_mData = {}

        for proc in procss:
            proc.join()

    info("We got all Files")


if __name__ == '__main__':
    getfileNames("pubmed/baseline/", "downloadFileBaseline.txt")
