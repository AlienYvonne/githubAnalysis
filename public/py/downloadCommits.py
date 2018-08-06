# 抓取一个repo下的所有commits
from urllib import request
import json
import re
import time
import os
import getURL

def getCommitData(src):
    dst = {}
    f = src['commit']
    dst['author'] = f['author']
    dst['committer'] = f['committer']
    dst['message'] = f['message']
    dst['comments_url'] = src['comments_url']
    dst['url'] = src['url']
    return dst

def fetchCommit(year,month,data,prefix):
    allUsers = {}
    if(os.path.exists(prefix+'allUsers.json')):
        with open(prefix + 'allUsers.json','r') as f:
            allUsers = json.loads(f.read())

    thisMonth = str(year) + "-" + "%02d" % month
    start = thisMonth + '-01T00:00:00Z'
    if(month == 12):
        end = thisMonth + "-31T23:59:59Z"
    else:
        end = str(year) + "-" +"%02d" % (month+1) + '-01T00:00:00Z'

    commitsUrl = data["commits_url"][0:-6] + "?since="+start+"&until="+end +"&access_token=8f6085fc4cf4b501a7ccad1a3aadc3f98f51384a"

    thisMonthUser = {}
    #time.sleep(3)
    commitsResponse =getURL.getURL(commitsUrl)
    #commitsData = commitsResponse.read().decode('utf-8')
    commitsData = json.loads(commitsResponse.data)
    # commitsData = getURL.getURL(commitsUrl)
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
            #time.sleep(3)
            commitsResponse = getURL.getURL(nextLink)#request.urlopen(nextLink)
            commitsData = commitsResponse.data
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

    with open(prefix + 'allUsers.json','w') as f:
        json.dump(allUsers,f)

def paddingCommit(year,month,data,prefix):
    thisMonth = str(year) + "-" + "%02d" % month

    with open(prefix + thisMonth + "-commitsUser.json",'w') as f:
        json.dump({},f)

    with open(prefix + thisMonth + "-commitsInfo.json",'w') as f:
        json.dump({},f)

    with open(prefix + thisMonth + "-originalCommits.json",'w') as f:
        json.dump({},f)

def getCommit(repo,startDate,endDate):
    prefix = 'public/data/' + repo + '/'
    print("I am downloadCommits.py.")
    print(prefix)

    url = 'https://api.github.com/repos/'+repo+"?access_token=8f6085fc4cf4b501a7ccad1a3aadc3f98f51384a"

    '''
    urlRequest = request.Request(url)
    urlResponse = request.urlopen(urlRequest)

    data = urlResponse.read().decode('utf-8')
    data = json.loads(data)
    '''
    data = json.loads(getURL.getURL(url).data)

    startDate = time.strptime(startDate[0:10],"%Y-%m-%d")
    endDate = time.strptime(endDate[0:10],"%Y-%m-%d")

    startYear = startDate.tm_year
    endYear = endDate.tm_year
    startMonth = startDate.tm_mon
    endMonth = endDate.tm_mon

    if(startYear == endYear):
        for month in range(startMonth,endMonth):
            fetchCommit(startYear,month,data,prefix)
        return

    for month in range(startMonth,13):
        fetchCommit(startYear,month,data,prefix)

    for year in range(startYear+1,endYear):
        for month in range(1,13):
            fetchCommit(year,month,data,prefix)

    for month in range(1,endMonth):
        fetchCommit(endYear,month,data,prefix)
    for month in range(endMonth,13):
        paddingCommit(endYear,month,data,prefix)
