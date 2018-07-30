# 寻找每个文件被几位开发者修改过 获得 AF 值
import json


def getOwnership(folder):
    cDir = "public/" + folder + "/"

    for year in range(2008,2019):
        ownerships = {}
        counts = {}

        for month in range(1,13):
            prefix = cDir + str(year) + "-" + "%02d" % month
            file = prefix +  "-modifiedFiles.json"

            with open(file,'r') as f:
                data = json.loads(f.read())
                for item in data:
                    filename = item["filename"]
                    user = item["user"]
                    if (filename not in counts):
                        counts[filename] = 0
                    if ( filename not in ownerships):
                        ownerships[filename] = {}
                    if ( user not in ownerships[filename]):
                        ownerships[filename][user] = 1
                        counts[filename] += 1
        A = 0
        B = 0
        for item in counts:
            sum = counts[item]
            A = A + sum
            B += 1
        if( B == 0):
             continue
        print(folder,"year:",year," ", "AF:",A/B)

getOwnership("json")
getOwnership("d3")
getOwnership("javascript")
