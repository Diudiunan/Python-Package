import pandas as pd
from FuckTree import *
from DrawTreePlotter import *

#测试数集函数
def HeHiHe(GET, ADATA):
    GTREE = GET[0]
    GBRANCH = GET[1]
    GSERIOUS = GET[2]
    AINDEX = ADATA.index
    Result = {}
    for inde in AINDEX:
        RE = ''
        for i in GTREE:
            TESTVALUE = ADATA.loc[inde, i.node]
            if i.node not in GSERIOUS.keys():
                if TESTVALUE == i.branch:
                    RE = GBRANCH[0]
                    break
                else:
                    RE = GBRANCH[1]
            elif i.branch != "无分支":
                try:
                    if TESTVALUE < float(i.branch[1:]):
                        RE = GBRANCH[0]
                        break
                    else:
                        RE = GBRANCH[1]
                except TypeError:
                    REMIND = "你的测试数据{0}不是连续性(数字)类型"
                    raise TypeError(REMIND.format(TESTVALUE))
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
DataFrameTree = GetDataFrame("Hipit int.csv")
GETGINIO = GetGini(DataFrameTree)
#GETGINIO = GetGini(DataFrameTree, root="是否有房")
#print(GETGINIO[:3])
DrawIT(GETGINIO)
"""print(GetGini(DataFrameTree, root="是否有房")[:2])
DataFrameTreeShrink = GetDataFrame(file="Hipit shrink.csv")
print(GetGini(DataFrameTreeShrink)[:2])"""
ROOT = '是否拖欠房贷'
Columns = ['是否有房', '婚姻状况', '年收入(单位:K)', '是否拖欠贷款']
SL1 = [["no", "single", 55, ""]]
#SL1 = [["", "single", "55K", "no"]]
#SL1 = [['yes', 'single', '125K', '']]
OP = pd.DataFrame(SL1, columns=Columns)
"""
#可以主动输入获得dataframe
OPL = givedataframe(Columns, root=ROOT)
"""
ColumnsR = HeHiHe(GETGINIO, OP)
print("你的输入为：{List}, 求{root}".format(List=SL1, root=ROOT))
print("结果字典为：{0}".format(ColumnsR))