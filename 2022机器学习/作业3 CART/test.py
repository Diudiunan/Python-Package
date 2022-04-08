import csv
import numbers

import numpy as np
import pandas as pd

#file="Hipit.csv"
#file="Hipit shrink.csv"
file="Hipit int.csv"
with open(file, encoding="UTF-8") as Reader:
    File_Csv = csv.reader(Reader)
    Csv_Head = next(File_Csv)
    print(Csv_Head)

DF = pd.read_csv(file, header=1, sep=Csv_Head[0], index_col=0)
print(DF)
print(DF.columns)
print((len(DF.columns)))
print(DF.columns[1])
for i in DF.columns:
    print(set(DF[i]))
print(set(DF[DF.columns[2]]))
"""dc = {"sd": "sd"}
print(dc['ef'])"""
"""def sd(sddf):
    print(sddf)

sd()"""
"""if "1":
    print("q")"""
dfg = {}
for i in DF.columns:
    dfg[i] = {}
    for j in DF[i]:
        dfg[i][j] = dfg[i].get(j, 0)+1
print(dfg)
print(dfg['是否拖欠贷款'].items())
print(sum(list(dfg['是否拖欠贷款'].values())))
index = pd.MultiIndex.from_product([[2013], ['yes', 'no']], names=["节点", "节点值"])
columns = pd.MultiIndex.from_product([["Bob"], ["yes", "no"]], names=["根", "根值"])
df = pd.DataFrame(index=index, columns=columns)
print(df)
gh = "是否有房"
dr = "是否拖欠贷款"
jf = ['yes', 'no']
for i in jf:
    for j in jf:
        df.loc[(2013, i), ('Bob', j)] = len(DF.loc[(DF[gh] == i) & (DF[dr] == j)])
print(df)
print(df.sum(axis=0))
print(df.sum().loc["Bob", "yes"])
print([i[1] for i in df.columns])
print([i[1] for i in df.index])
print(df.loc[2013, ("Bob", "yes")])
print(df.loc[(2013, "no"), ("Bob", "yes")])
idx = pd.IndexSlice
rop = df.loc[:, ("Bob", ["yes", "no"])]
print(rop.sum(axis=1))
print(rop.sum(axis=1).loc[2013, "yes"])
print("test over")
print(DF)
"""print(DF.loc[DF["婚姻状况"] != "married", ["是否有房", "婚姻状况", "年收入"]])
print(DF.loc[(DF["年收入"] != "(120-140K)") & (DF["婚姻状况"] != "married"), ["是否有房", "婚姻状况", "年收入"]])
print("sd\nsd")
Columns = ['是否有房', '婚姻状况', '年收入', '是否拖欠房贷']
SL1 = [["无", "single", "55K", ""]]
OP = pd.DataFrame(SL1, columns=Columns)
print(OP)"""
for i in DF.columns:
    if "单位" in i and DF[i].dtype in ["int64", "float64", "complex128"]:
        print(i)
print(DF["年收入(单位:K)"])
print(DF["年收入(单位:K)"][1])
print(isinstance(DF["年收入(单位:K)"][1], numbers.Real))
print(1-(1/2)**2-(1/2)**2)