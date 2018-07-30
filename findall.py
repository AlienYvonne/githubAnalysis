from urllib import request
import json
import re #正则表达式

def getNextLink(data):
    nextLink = re.findall(r'<*>*rel="next"',data)
    print(nextLink)

def getUserInfo(url):
    url_request = request.Request(url)
    url_response = request.urlopen(url)
    print(url_request.get_method())
    print(url_response.info())
    data = url_response.read().decode('utf-8')
    #
def getUrlResponse(url):
    url_request = request.Request(url)
    url_response = request.urlopen(url)

    return url_response

def addCommitInfo(data):
    print(data)

def getCommitInfo(repo):
    url = "https://api.github.com/search/commits?q=repo:octocat/Spoon-Knife+css"
    print(url)
    urlRequest = request.Request(url)
    urlRequest.add_header('Accept','application/vnd.github.cloak-preview')
    print(urlRequest)

    urlResponse = request.urlopen(urlRequest)
    #headData = urlResponse.getheaders()
    headData = urlResponse.info()
    data = urlResponse.read().decode('utf-8')
    print(data)

    '''
    nextLink = getNextLink(data)
    while(nextLink != null):
        addCommitInfo(data)
        urlResponse = request.urlopen(nextLink)
        data = urlResponse.read().decode('utf-8')
        nextLink = getNextLink(data)
    addCommitInfo(data)
    '''


def getIssueInfo(url):
    url_request = request.Request(url)
    url_response = request.urlopen(url)
    print(url_request.get_method())
    print(url_response.info())
    data = url_response.read().decode('utf-8')

    #link_list = re.findall(r'Link:<*rel="next"',data)
    #print(link_list)
    #url_response.read().decode('utf-8'))

def getRepoInfo(repo):
    url =  'https://api.github.com/repos/'+repo
    print(url)
    urlRequest = request.Request(url)

    urlResponse = request.urlopen(urlRequest)
    #headData = urlResponse.getheaders()
    data = urlResponse.read().decode('utf-8')
    data = json.loads(data)
    print(urlResponse.headers)

    with open("repoInfo.json",'w') as f:
        json.dump(data,f)

baseRepo = 'atom/atom'

getRepoInfo(baseRepo)

# getIssueInfo(baseUrl)

'''
request.Request(baseUrl)
link_list = request
with request.urlopen(baseUrl) as f:
    data = f.read()
    print(f.headers)

    #data.decode('utf-8')
    #data = json.loads(data)

#with open("test2.json",'w') as f:
    #json.dump(data,f)
'''
