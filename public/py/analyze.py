import json
import attraction
import findTenure
import contribution
import ownership

def analyzeCommits(repo,start,end):
    print("I am analyzeCommits.")

    startYear = int(start[0:4])
    startMonth = start[5:7]
    endYear = int(end[0:4])
    endMonth = end[5:7]

    # 生成所需要的数据

    # 项目吸引力的度量
    # 每月新开发者 /外部开发者的进入率 柱状图
    attraction.merge(repo,endYear)

    # 开发者持续贡献性的度量
    # 统计任期，绘制每月任期图 柱状图
    findTenure.findTenure(repo)

    # 团队多样性的度量
    # 分析代码贡献率 核心团队规模 扇形图
    contribution.findCon(repo,endYear,startYear,startMonth,endYear,endMonth)

    # 项目规范性的度量
    # 计算AF值

    ownership.getOwnership(repo)


def analyze(repo,start,end):
    analyzeCommits(repo,start,end)
