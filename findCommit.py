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
    return dst

def getCommit(repo):

    url = 'https://api.github.com/repos/'+repo+"?access_token=8f6085fc4cf4b501a7ccad1a3aadc3f98f51384a"
    print("url:",url)
    urlRequest = request.Request(url)
    urlResponse = request.urlopen(urlRequest)

    data = urlResponse.read().decode('utf-8')
    data = json.loads(data)
    rangeDate = []
    dayDate = []

    for j in range(1,10):
        dayDate.append('0'+str(j) )
    for j in range(10,13):
        dayDate.append(str(j))
    dayDate.append("12-31T23:59:59Z")
    print(dayDate)
    allUsers = {}

    for i in range(2008,2019): # 每年
        for j in range(0,12):
            thisMonth = str(i) + "-" + dayDate[j]
            start = thisMonth + '-01T00:00:00Z'
            if j == 11:
                end =  str(i) + "-" + dayDate[j+1]
            else :
                end = str(i) + "-" + dayDate[j+1] + '-01T00:00:00Z'
            commitsUrl = data["commits_url"][0:-6] + "?since="+start+"&until="+end +"&access_token=8f6085fc4cf4b501a7ccad1a3aadc3f98f51384a"
            print(commitsUrl)

            thisMonthUser = {}
            time.sleep(5)
            commitsResponse = request.urlopen(commitsUrl)
            commitsData = commitsResponse.read().decode('utf-8')
            commitsData = json.loads(commitsData)
            countCommits = 0
            dealdData = []
            headData = str(commitsResponse.headers)
            print(headData)
            countCommits += len(commitsData)

            with open(thisMonth + "-originalCommits.json",'w') as f:
                json.dump(commitsData,f)

            for item in commitsData:
                tmpData = getCommitData(item)
                dealdData.append(tmpData)

            while True:
                listLink = re.findall(r'(?<=<).[^<]*(?=>; rel=\"next)',headData)
                print("listLink: " , listLink)
                if(listLink):
                    nextLink = listLink[0]
                    print("nextLink: " , nextLink)
                    time.sleep(5)
                    commitsResponse = request.urlopen(nextLink)
                    commitsData = commitsResponse.read().decode('utf-8')
                    commitsData = json.loads(commitsData)
                    headData = str(commitsResponse.headers)
                    print(headData)
                    countCommits += len(commitsData)
                    for item in commitsData:
                        tmpData = getCommitData(item)
                        dealdData.append(tmpData)
                    with open(thisMonth + "-originalCommits.json",'a') as f:
                        json.dump(commitsData,f)
                else:
                    break
            for item in dealdData:
                user = str(item['author']['email'])
                commitInfo = {}
                commitInfo['date'] = item['author']['date']
                commitInfo['message'] = item['message']
                if( user not in thisMonthUser ):
                    thisMonthUser[user] = []
                if( user not in allUsers):
                    allUsers[user] = []
                thisMonthUser[user].append(commitInfo)
                allUsers[user].append(commitInfo)

            with open(thisMonth + "-commitsUser.json",'w') as f:
                json.dump(thisMonthUser,f)

            with open(thisMonth + "-commitsInfo.json",'w') as f:
                json.dump(dealdData,f)
            '''

    with open("repoInfo.json",'w') as f:
        json.dump(data,f)
    with open("commitsUser.json",'w') as f:
        json.dump(allUsers,f)
        '''


def plot():
    with open("commitsUser.json",'r') as f:
        commitsUser = json.load(f)
    for user in commitsUser:
        commitInfo = commitsUser[user]
        date = commitInfo['date']
def getIssue(repo):
    url = 'https://api.github.com/repos/'+repo+"?access_token=8f6085fc4cf4b501a7ccad1a3aadc3f98f51384a"

    urlRequest = request.Request(url)
    urlResponse = request.urlopen(urlRequest)

    data = urlResponse.read().decode('utf-8')
    data = json.loads(data)
    rangeDate = []
    for i in range(2008,2020):
        rangeDate.append(str(i) + '-01-01T00:00:00Z')

    #for i in range(len(rangeDate)-1):
    start = rangeDate[i]
    end = rangeDate[i+1]

    #处理已关闭的Issue
    closedIssue = {}
    #处理未关闭的Issue
    openIssue = {}
    #处理pull request
    closedPull = {}
    #
    openPull = {}
    issueUrl = data["issue_events_url"][0:-9] +"?state=closed""&access_token=8f6085fc4cf4b501a7ccad1a3aadc3f98f51384a"
    print("issueUrl: ", issueUrl)
    issueResponse = request.urlopen(issueUrl)
    issueData = issueResponse.read().decode('utf-8')
    issueData = json.loads(issueData)

    with open("isssuEventClosed.json",'w') as f:
        json.dump(issueData,f)

    headData = str(issueResponse.headers)
    print("headData: ", headData)

    while(True):
        listLink = re.findall(r'(?<=<).[^<]*(?=>; rel=\"next)',headData)
        print("listLink: ", listLink)

        if listLink:
            nextLink = listLink[0]
            print("nextLink: ", nextLink)
            time.sleep(5)
            issueResponse = request.urlopen(nextLink)
            issueData = issueResponse.read().decode('utf-8')
            issueData = json.loads(issueData)

            with open("isssuEvent.json",'a') as f:
                json.dump(issueData,f)
            headData = str(issueResponse.headers)
            print("headData:", headData)

        else:
            break


baseRepo = ["d3/d3"] #"kapilratnani/JSON-Viewer"]#"nlohmann/json"]#]#,"atom/atom"]
for item in baseRepo:
   getCommit(item)

#plot()
#for item in baseRepo:
#    getIssue(item)
