# 统计每个开发者的贡献比例

import urllib
from urllib import request
import json
import urllib
import getURL
def getModified(cDir,year,month,modifiedInfo):

    prefix = cDir + str(year) + "-" + "%02d" % month

    file = prefix + "-commitsInfo.json"

    with open(file,"r") as f:
        data = f.read()
        data = json.loads(data)
    modifiedInfo = []

    for commit in data:
        commitUrl = commit["url"]

        #print("commitUrl:",commitUrl)
        urlResponse = getURL.getURL(commitUrl)
        #urlResponse = request.urlopen(commitUrl + "?access_token=8f6085fc4cf4b501a7ccad1a3aadc3f98f51384a")
        commitInfo = json.loads(urlResponse.data)
        #commitInfo = getURL.getURL(commitUrl)

        user = commitInfo["commit"]["author"]["email"]
        date = commitInfo["commit"]["author"]["date"]

        modifiedFiles = commitInfo["files"]

        for i in range(0,len(modifiedFiles)):
            if("patch" in modifiedFiles[i]):
                modifiedFiles[i].pop("patch")
            modifiedFiles[i]["user"] = user
            modifiedFiles[i]["date"] = date

        modifiedInfo = modifiedInfo + modifiedFiles

    with open(prefix + "-modifiedFiles.json","w") as f:
        json.dump(modifiedInfo,f)

def findCon(folder,startYear,startMonth,endYear,endMonth):
    cDir = "public/data/" + folder + "/"
    print("I am findCon.")

    if(startYear == endYear):
        for month in range(startMonth,endMonth):
            getModified(cDir,startYear,month)
        return

    for month in range(startMonth,13):
        getModified(cDir,startYear,month)

    for year in range(startYear+1,endYear):
        for month in range(1,13):
            getModified(cDir,year,month)

    for month in range(1,endMonth):
        getModified(cDir,endYear,month)
