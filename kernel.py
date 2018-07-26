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
            print(file)
            with open(file,"r") as f:
                data = f.read()
                data = json.loads(data)

            for commit in data:
                commitUrl = commit["url"]
                print(commitUrl)
                count += 1
                print("count:")
                time.sleep(1)
                urlResponse = request.urlopen(commitUrl + "?access_token=8f6085fc4cf4b501a7ccad1a3aadc3f98f51384a")
                commitInfo = json.loads(urlResponse.read().decode("utf-8"))

                user = commitInfo["commit"]["author"]["email"]
                modifiedFiles = commitInfo["files"]

                for i in range(0,len(modifiedFiles)):
                    if("patch" in modifiedFiles[i]):
                        modifiedFiles[i].pop("patch")

                if(user not in modifiedInfo):
                    modifiedInfo[user] = []
                modifiedInfo[user] = modifiedInfo[user] + modifiedFiles

    with open(prefix + "-modifiedInfo.json",'w') as f:
        json.dump(modifiedInfo,f)

folders = ["JSON","d3"]

for folder in folders:
    findCon(folder)
