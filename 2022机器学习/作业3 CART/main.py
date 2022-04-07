import pandas as pd
from FuckTree import *
from DrawTreePlotter import *

def HeHiHe(GET, ADATA):
    GTREE = GET[0]
    GBRANCH = GET[1]
    AINDEX = ADATA.index
    Result = {}
    for inde in AINDEX:
        RE = ''
        for i in GTREE:
            if ADATA.loc[inde, i.node] == i.branch:
                RE = GBRANCH[0]
            else:
                RE = GBRANCH[1]
        Result[inde] = RE
    return Result

def givedataframe(Columns, root):
    LIST = []
    TIME = 1
    while 1:
        print("第{}轮输入".format(TIME))
        List = []
        for i in Columns:
            if i != root:
                INPUT = input("请输入：{}".format(i))
                List.append(INPUT)
                if INPUT == "Q":
                    break
            else:
                List.append("")
        LIST.append(List)
        TIME += 1
    INPUTDATA = pd.DataFrame(LIST, index=[i for i in TIME], columns=Columns)
    return INPUTDATA

help()
DataFrameTree = GetDataFrame()
GETGINIO = GetGini(DataFrameTree)
print(GETGINIO[:2])
DrawIT(GETGINIO)
"""print(GetGini(DataFrameTree, root="是否有房")[:2])
DataFrameTreeShrink = GetDataFrame(file="Hipit shrink.csv")
print(GetGini(DataFrameTreeShrink)[:2])"""
ROOT = '是否拖欠房贷'
Columns = ['是否有房', '婚姻状况', '年收入', '是否拖欠房贷']
SL1 = [["no", "single", "55K", ""]]
#SL1 = [['yes', 'single', '125K', '']]
OP = pd.DataFrame(SL1, columns=Columns)
"""
#可以主动输入获得dataframe
OPL = givedataframe(Columns, root=ROOT)
OP = pd.DataFrame(SL1, columns=Columns)
"""
ColumnsR = HeHiHe(GETGINIO, OP)
print("你的输入为：{List}, 求{root}".format(List=SL1, root=ROOT))
print("结果字典为：{0}".format(ColumnsR))