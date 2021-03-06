import sys
import os
import downloadCommits
import downloadIssues
import downloadComments
import datetime
import time
import analyze
from urllib import request
import numpy as np
import urllib
import json

def mkdir(path):
    flag = os.path.exists(path)
    if(not flag):
        os.makedirs(path)


print(sys.argv)

repo = sys.argv[1]
start = sys.argv[2]
end = sys.argv[3]
'''
paras = ["nlohmann/json","2008-01-01","2018-08-08"]
repo = paras[0]
start = paras[1]
end = paras[2]
'''
# 判断该仓库是否在github上存在

try:
    url = 'https://api.github.com/repos/'+repo
    urlRequest = request.Request(url)
    urlResponse = request.urlopen(urlRequest)

    data = urlResponse.read().decode('utf-8')
    data = json.loads(data)
    print(data)

except urllib.error.HTTPError:
    print(url)
    print('No such repo.')
    sys.exit()
except urllib.error.URLError:
    print('No such repo.')
    sys.exit()


# 新建文件存放目录
path = './public/data/' + repo + '/'
mkdir(path);

# 新建timeStampStart，保存下载开始时间
with open(path+'/timeStampStart','w') as f:
    timeStamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f.write(timeStamp)

# 下载所有commits
downloadCommits.getCommit(repo,start,end)

# 下载所有Issues
downloadIssues.getIssues(repo,end)

# 下载所有comments
downloadComments.downloadComments(repo,start,end)

#对数据进行分析 分析时是对所有的数据
analyze.analyze(repo,start,end)

# 生成timeStampEnd文件保存更新时间
'''
with open(path+'/timeStampEnd','w') as f:
    timeStamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(timeStamp)
    f.write(timeStamp)
'''
