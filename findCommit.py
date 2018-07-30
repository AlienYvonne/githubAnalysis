# 抓取一个repo下的所有commits
from urllib import request
import json
import re
import time

def getCommitData(src):
    dst = {}
    f = src['commit']
    dst['author'] = f['author']
    dst['committer'] = f['committer']
    dst['message'] = f['message']
    dst['comments_url'] = src['comments_url']
    dst['url'] = src['url']
    return dst

def getCommit(repo):
    if(repo == "d3/d3"):
        prefix = "public/d3/"
    elif (repo == "json"):
        prefix = "public/JSON/"
    elif( repo == "airbnb/javascript"):
        prefix = "public/javascript/"

    url = 'https://api.github.com/repos/'+repo+"?access_token=8f6085fc4cf4b501a7ccad1a3aadc3f98f51384a"

    print("url:",url)
    urlRequest = request.Request(url)
    urlResponse = request.urlopen(urlRequest)

    data = urlResponse.read().decode('utf-8')
    data = json.loads(data)


    allUsers = {}

    for year in range(2008,2019): # 每年
        for month in range(1,13):

            thisMonth = str(year) + "-" + "%02d" % month
            start = thisMonth + '-01T00:00:00Z'
            if(month == 12):
                end = thisMonth + "-31T23:59:59Z"
            else:
                end = str(year) + "-" +"%02d" % (month+1) + '-01T00:00:00Z'

            commitsUrl = data["commits_url"][0:-6] + "?since="+start+"&until="+end +"&access_token=8f6085fc4cf4b501a7ccad1a3aadc3f98f51384a"

            print(commitsUrl)

            thisMonthUser = {}
            time.sleep(3)
            commitsResponse = request.urlopen(commitsUrl)
            commitsData = commitsResponse.read().decode('utf-8')
            commitsData = json.loads(commitsData)
            countCommits = 0
            dealdData = []

            headData = str(commitsResponse.headers)

            originalCommits = commitsData

            for item in commitsData:
                tmpData = getCommitData(item)
                dealdData.append(tmpData)

            while True:
                listLink = re.findall(r'(?<=<).[^<]*(?=>; rel=\"next)',headData)
                print("listLink: " , listLink)
                if(listLink):
                    nextLink = listLink[0]
                    print("nextLink: " , nextLink)
                    time.sleep(3)
                    commitsResponse = request.urlopen(nextLink)
                    commitsData = commitsResponse.read().decode('utf-8')
                    commitsData = json.loads(commitsData)
                    originalCommits = originalCommits + commitsData

                    headData = str(commitsResponse.headers)

                    for item in commitsData:
                        tmpData = getCommitData(item)
                        dealdData.append(tmpData)

                else:
                    break

            for item in dealdData:
                user = str(item['author']['email'])
                commitInfo = {}
                commitInfo['date'] = item['author']['date']
                commitInfo['message'] = item['message']
                commitInfo['url'] = item["url"]

                if( user not in thisMonthUser ):
                    thisMonthUser[user] = []
                if( user not in allUsers):
                    allUsers[user] = []
                thisMonthUser[user].append(commitInfo)
                allUsers[user].append(commitInfo)

            with open(prefix + thisMonth + "-commitsUser.json",'w') as f:
                json.dump(thisMonthUser,f)

            with open(prefix + thisMonth + "-commitsInfo.json",'w') as f:
                json.dump(dealdData,f)

            with open(prefix + thisMonth + "-originalCommits.json",'w') as f:
                json.dump(originalCommits,f)

    with open("allUsers.json","w") as f:
        json.dump(allUsers,f)


baseRepo = ["airbnb/javascript"]#]"d3/d3"] #"nlohmann/json",]#,"atom/atom"]
for item in baseRepo:
   getCommit(item)
