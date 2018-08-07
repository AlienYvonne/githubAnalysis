import json
import getURL
import shutil
import os
import divideCommentsMonth
import requests
from urllib import request
import re
import time

def getAllComments(repo):
    cDir = "public/data/" + repo+ "/" + "comments/"
    if(os.path.exists(cDir)):
        shutil.rmtree(cDir)
    os.makedirs(cDir)
    url = 'https://api.github.com/repos/'+repo+ \
            "/comments?access_token=8f6085fc4cf4b501a7ccad1a3aadc3f98f51384a"
    urlRequest = request.Request(url)
    urlResponse = request.urlopen(urlRequest)
    commentsData = json.loads(urlResponse.read().decode("utf-8"))
    page = 1

    with open(cDir + "allComments-" + str(page) + ".json","w",newline="") as f:
        json.dump(commentsData,f)

    headData = str(urlResponse.headers)
    while True:
        listLink = re.findall(r'(?<=<).[^<]*(?=>; rel=\"next)',headData)
        print("listLink: " , listLink)
        if(listLink):
            nextLink = listLink[0]
            print("nextLink: " , nextLink)
            time.sleep(1)
            page += 1
            commentsResponse = request.urlopen(nextLink)
            commentsData = commentsResponse.read().decode('utf-8')
            commentsData = json.loads(commentsData)

            with open(cDir + "allComments-" + str(page) + ".json","w",newline="") as f:
                json.dump(commentsData,f)

            headData = str(commentsResponse.headers)

        else:
            break


def downloadComments(repo,startDate,endDate):
    # 下载所有commit comment
    getAllComments(repo)

    # 下载所有issue comment * issues/comments

    endDate = time.strptime(endDate[0:10],"%Y-%m-%d")
    endYear = endDate.tm_year
    divideCommentsMonth.divideCommentsMonth(repo,endYear)
