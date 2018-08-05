# 统计每个开发者的贡献比例

from urllib import request
import json
import time

def findCon(folder):
    cDir = "public/" + folder + "/"

    modifiedInfo = {}
    count = 0

    for year in range(2008,2019):
        for month in range(1,13):

            prefix = cDir + str(year) + "-" + "%02d" % month

            file = prefix + "-commitsInfo.json"

            with open(file,"r") as f:
                data = f.read()
                data = json.loads(data)
            modifiedInfo = []

            for commit in data:
                commitUrl = commit["url"]
                print(commitUrl)
                count += 1
                print("count:",count)
                time.sleep(2)
                urlResponse = request.urlopen(commitUrl + "?access_token=8f6085fc4cf4b501a7ccad1a3aadc3f98f51384a")
                commitInfo = json.loads(urlResponse.read().decode("utf-8"))

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
            print(prefix)


folders = ["javascript"]#"d3"]

for folder in folders:
    findCon(folder)
