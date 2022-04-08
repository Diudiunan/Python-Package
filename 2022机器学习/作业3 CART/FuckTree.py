import csv
from collections import namedtuple
import numpy as np
import pandas as pd


class CTree():

    def __init__(self, DataFrame, root=-1):
        self.data = DataFrame
        self.index = DataFrame.columns
        #排序列内元素集合
        #排序的不同会对后期树的分支抉择产生影响
        """self.dict_set = {i: sorted(list(set(DataFrame[i])), reverse=True)
                         for i in DataFrame.columns}"""
        self.dict_set = {i: sorted(list(set(DataFrame[i])))
                         for i in DataFrame.columns}
        self.dict_num = {}
        self.__alternate = {}
        self.serialcolumns = {}
        if root == -1:
            self.root = {"rootname": self.index[root], "rootgini": 0, "giniget": False}
        else:
            if root in self.index:
                self.root = {"rootname": root, "rootgini": 0, "giniget": False}
            else:
                raise "The key named {0} doesn't exist！".format(root)

    def give_dict(self):                                             #获得每类属性内各种值的总数
        for i in self.index:
            self.dict_num[i] = {}
            for j in self.data[i]:
                self.dict_num[i][j] = self.dict_num[i].get(j, 0) + 1

    def isserialcolumns(self):                                       #判断是否有列值为连续
        for i in self.index:
            if "单位" in i and self.data[i].dtype in ["int64", "float64", "complex128"]:
                SortList = sorted([i for i in self.data[i]])
                MidValueList = [(SortList[i]+SortList[i+1])/2
                                for i in range(len(SortList)-1)]
                print(MidValueList)
                self.serialcolumns[i] = {"sortlist": SortList,
                                         "midvaluelist": MidValueList}
        return self.serialcolumns

    @property
    def give_alternateDF(self):                                      #获得多级索引交叉表
        DictMultiFrame = {}
        root = self.root["rootname"]
        dictsetrootlist = self.dict_set[root]
        for LongitudinalName in self.index:
            if LongitudinalName != root:
                dictsettolist = self.dict_set[LongitudinalName]
                index = pd.MultiIndex.from_product([[root],
                                                    dictsetrootlist],
                                                   names=["根", "根值"])
                columns = pd.MultiIndex.from_product([[LongitudinalName],
                                                      dictsettolist],
                                                     names=["节点", "节点值"])
                df = pd.DataFrame(index=index, columns=columns)
                for i in dictsetrootlist:
                    for j in dictsettolist:
                        df.loc[(root, i), (LongitudinalName, j)] = \
                            len(self.data.loc[(self.data[root] == i) &
                                              (self.data[LongitudinalName] == j)])
                        DictMultiFrame[(root, LongitudinalName)] = df
        self.__alternate = DictMultiFrame
        return self.__alternate

    def Gini(self):
        if not self.dict_num:
            self.give_dict()
        if not self.serialcolumns:
            self.isserialcolumns()
        if not self.root["giniget"]:                                 #根gini值判空
            RootList = list(self.dict_num[self.root["rootname"]].values())
            RootListSum = sum(RootList)
            GiniNumber = 1
            for i in RootList:
                GiniNumber -= (i / RootListSum) ** 2
            self.root["rootgini"] = GiniNumber
            print(GiniNumber)
            self.root["giniget"] = True
            return self.Gini()
        else:
            RootGini = self.root["rootgini"]                         #根部Gini值
            DictGini = {}                                            #定义Gini系数字典
            if not self.__alternate:                                 #确保多级索引划分完毕
                self.give_alternateDF
            for key, data in self.__alternate.items():               #开始遍历计算根下属性
                print(data)
                Attributedictionary = {}                             #定义属性系数字典
                datacolumns = [p[1] for p in data.columns]           #获得多级索引内柱
                dataindexs = [p[1] for p in data.index]              #获得多级索引行栏
                sumaxis0 = data.sum(axis=0)                          #获得每列数值和
                #列-数值和字典
                dictsumaxis0 = {i: sumaxis0.loc[key[1], i]
                                for i in datacolumns}
                DenominatorSum = sum(dictsumaxis0.values())          #总和
                #连续值列的单独处理
                if self.serialcolumns and key[1] in self.serialcolumns.keys():
                    midColumns = self.serialcolumns[key[1]]["midvaluelist"]
                    for midv in midColumns:
                        #获得小于中值midv的所有列
                        itsmycolumns = [i for i in datacolumns if i < midv]
                        itsmydata = data.loc[:, (key[1], itsmycolumns)]
                        mysum0 = itsmydata.sum(axis=0)               #每列和
                        mysum1 = itsmydata.sum(axis=1)               #每行和
                        dictmysum0 = {i: mysum0.loc[key[1], i]
                                for i in itsmycolumns}
                        itsmysum = sum(dictmysum0.values())
                        selfrate_s = itsmysum/DenominatorSum
                        selfgini_s = 1
                        for me in dataindexs:
                            selfgini_s -= (mysum1.loc[key[0], me] /
                                           itsmysum) ** 2
                        #获得大于中值midv的所有列
                        notmycolumns = [i for i in datacolumns if i >= midv]
                        notmydata = data.loc[:, (key[1], notmycolumns)]
                        othersum0 = notmydata.sum(axis=0)            #每列和
                        othersum1 = notmydata.sum(axis=1)            #每行和
                        dictothersum0 = {i: othersum0.loc[key[1], i]
                                      for i in notmycolumns}
                        itsothersum = sum(dictothersum0.values())
                        otherrate_s = 1 - selfrate_s
                        othergini_s = 1
                        for me in dataindexs:
                            othergini_s -= (othersum1.loc[key[0], me] /
                                           itsothersum) ** 2
                        GiniOfFna = RootGini - \
                                    selfrate_s * selfgini_s - \
                                    otherrate_s * othergini_s
                        Attributedictionary[midv] = GiniOfFna        #一个gini值
                else:  #通用离散处理
                    for Gna in datacolumns:                          #遍历多级索引的内柱
                        selfrate = dictsumaxis0[Gna]/DenominatorSum  #内部比例
                        selfgini = 1
                        for me in dataindexs:                        #内层Gini减数
                            selfgini -= (data.loc[(key[0], me), (key[1], Gna)] /
                                              dictsumaxis0[Gna]) ** 2
                        otherrate = 1 - selfrate                     #外部比例
                        othergini = 1
                        #接下来去除Gna柱并获得行栏和
                        othercolumns = [i for i in datacolumns if i != Gna]
                        # 去除Gna柱的data
                        otherdata = data.loc[:, (key[1], othercolumns)]
                        otheraxis1 = otherdata.sum(axis=1)           #获得行栏和
                        dictotheraxis1 = {i: otheraxis1.loc[key[0], i]
                                          for i in dataindexs}
                        Denominatorother = sum(dictotheraxis1.values())
                        for they in dataindexs:                      #外层Gini减数
                            othergini -= (dictotheraxis1[they] /
                                          Denominatorother) ** 2
                        GiniOfFna = RootGini - \
                                    selfrate * selfgini - \
                                    otherrate * othergini
                        Attributedictionary[Gna] = GiniOfFna         #一个gini值
                DictGini[key] = Attributedictionary
            return DictGini

    #  下列为一个内部循环生产函数，由于牵涉到类的内部修改故而放弃，以计留念
    """def GetGini(self):
        # 嘿嗨嘿，兄弟们！开涮！！！
        RootGroupList = [i for i in self.index]
        BranchTuple = namedtuple("Branch", "level node branch gini")
        RootGroupList.remove(self.root["rootname"])
        BranchList = []
        for i in range(len(self.index) - 1):
            GetDict = self.Gini()
            Mixdict = {"key": '', "attr": '', "MixValue": 0}
            for key, value in GetDict.items():
                for attr, gini in value.items():
                    if Mixdict["MixValue"] < gini:
                        Mixdict["key"] = key[1]
                        Mixdict["attr"] = attr
                        Mixdict["MixValue"] = gini
            BranchList.append(BranchTuple(i, Mixdict["key"],
                                          Mixdict["attr"], Mixdict["MixValue"]))
            self.root["rootname"] = Mixdict["key"]
            self.root["rootgini"] = 0
            self.root["giniget"] = True
            self.data = self.data.loc[
                self.data[Mixdict["key"]] != Mixdict["attr"], RootGroupList]
            RootGroupList.remove(Mixdict["key"])
        return BranchList"""

    """@property
    def GiniTree(self):
        return self.GetGini()"""

def GetGini(DataFrame, root=-1):
    #嘿嗨嘿，兄弟们！开涮！！！
    data = DataFrame
    Onectree = CTree(data, root)
    BranchPoint = tuple(Onectree.dict_set[Onectree.root["rootname"]])
    RootGroupList = [i for i in Onectree.index]
    BranchTuple = namedtuple("Branch", "level node branch gini")
    #RootGroupList.remove(Onectree.root["rootname"])
    AllGiniDictList = []
    BranchList = []
    OutSetLen = len(Onectree.index)
    for i in range(OutSetLen-1):
        GetDict = Onectree.Gini()
        AllGiniDictList.append(GetDict)
        Mixdict = {"key": '', "attr": '', "MixValue": 0}
        #为了满足要求：同大gini 则取前值。如果取后值请注释上下行->
        MAXLISTPATTERN = max([gini for value in GetDict.values()
                              for gini in value.values()])
        GETAMIX = False
        #<-
        for key, value in GetDict.items():
            for attr, gini in value.items():
                if GETAMIX:#如果取后值请注释
                    break
                if gini == MAXLISTPATTERN:
                    Mixdict["key"] = key[1]
                    Mixdict["attr"] = attr
                    Mixdict["MixValue"] = gini
                    # 如果取后值请注释
                    GETAMIX = True
        #如果后续无法分支，则
        if Mixdict["MixValue"] == 0:
            Mixdict["attr"] = "无分支"
        BranchList.append(BranchTuple(i, Mixdict["key"],
                                      Mixdict["attr"], Mixdict["MixValue"]))
        try:
            RootGroupList.remove(Mixdict["key"])
        except ValueError:
            print("没有找到{}".format(Mixdict["key"]))
        data = data.loc[data[Mixdict["key"]] != Mixdict["attr"], RootGroupList]
        Onectree = CTree(data, root=root)
    return BranchList, BranchPoint, AllGiniDictList

def GetDataFrame(file="Hipit.csv"):
    with open(file, encoding="UTF-8") as Reader:
        File_Csv = csv.reader(Reader)
        Csv_Head = next(File_Csv)

    DF = pd.read_csv(file, header=1, sep=Csv_Head[0], index_col=0)
    return DF

def help():
    STR = "使用函数GetGini(dataframe[,root=name])，root默认为dataframe最后一列名，" \
          "\n如需修改请设置其参数名。注意！主根内仅可有两类值，即其集合长度为2." \
          "\n此方法为作者闭门造车之产物，疏漏之处难以为一人估量，望使用者多多包涵。" \
          "\n{name:->70}"
    print(STR.format(name="Diudiunan"))

if __name__ == "__main__":
    DataFrameTree = GetDataFrame("Hipit int.csv")
    #MyTree = CTree(DataFrameTree)
    #print(MyTree.dict_set)
    #print(MyTree.isserialcolumns())
    #print(MyTree.give_alternateDF)
    """print(MyTree.dict_num)
    lois = MyTree.give_alternateDF.items()
    for k, v in lois:
        print(v)
        print(v.columns)
        print([p[1] for p in v.columns])"""
    #print(MyTree.Gini())
    #print(MyTree.GiniTree)
    print(GetGini(DataFrameTree)[:])
    """
    print(GetGini(DataFrameTree, root="是否有房")[:2])
    DataFrameTreeShrink = GetDataFrame(file="Hipit shrink.csv")
    print(GetGini(DataFrameTreeShrink)[:2])"""
    help()


