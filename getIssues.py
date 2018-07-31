# 获取一个repo里所有Issue的情况
import json
import os
import requests
from urllib import request
import re
import time

def getIsssues(repo):
    repos = repo.split(sep="/")
    organ = repos[0]
    folder = repos[1]

    cDir = "public/" + folder + "/" + "issues/"
    isExists = os.path.exists(cDir)
    if not isExists:
        os.makedirs(cDir)

    url = 'https://api.github.com/repos/'+repo+ \
            "/issues?access_token=8f6085fc4cf4b501a7ccad1a3aadc3f98f51384a" \
            "&state=all&filter=all"
    urlRequest = request.Request(url)
    urlResponse = request.urlopen(urlRequest)
    issuesData = json.loads(urlResponse.read().decode("utf-8"))
    page = 1

    with open(cDir + "allIssues-" + str(page) + ".json","w",newline="") as f:
        json.dump(issuesData,f)

    headData = str(urlResponse.headers)
    while True:
        listLink = re.findall(r'(?<=<).[^<]*(?=>; rel=\"next)',headData)
        print("listLink: " , listLink)
        if(listLink):
            nextLink = listLink[0]
            print("nextLink: " , nextLink)
            time.sleep(2)
            page += 1
            issuesResponse = request.urlopen(nextLink)
            issuesData = issuesResponse.read().decode('utf-8')
            issuesData = json.loads(issuesData)

            with open(cDir + "allIssues-" + str(page) + ".json","w",newline="") as f:
                json.dump(issuesData,f)

            headData = str(issuesResponse.headers)

        else:
            break



repos = ["d3/d3","airbnb/javascript","nlohmann/json"]

for item in repos:
    getIsssues(item)
