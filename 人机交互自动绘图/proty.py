#
"""
这是一个具有读取规则并应用规则对过滤后的数据进行处理的
类库
"""

#
"""
引用
"""

import json
import re
import copy


#读取规则与返回
class GetR:
    
    def __init__(self, File='proty.json'):  #需设置一个默认规则文件
        self.file = File
        self.dict = {}
        
    def GetRules(self):
        #读取文件
        with open(self.file, 'r') as OPFL:
            Json_Dict = json.load(OPFL)
        return Json_Dict


#公式的过滤与匹配
class GoBacker:
    
    def __init__(self, Str, Dict_Rules):
        self.STR = Str
        self.RULES = Dict_Rules

    """严格输入可直接使用正则替换函数"""
    #正则替换
    def Regular_Replace(self):
        Pattern_List =[i for i in self.RULES.keys()]
        Set_MatchStr = re.sub(r"|".join(Pattern_List),
                              lambda x: self.RULES[x.group()][0], self.STR)
        return Set_MatchStr

    """输入不严格时采用以下函数"""
    #分解公式
    def GetString(self):
        GS_Str = self.STR
        GS_Rules = self.RULES

        
        #括号分解
        def Get_Bracket(Str):
            L_Bracket = r'\('
            R_Bracket = r'\)'
            L_Bracket_List = [list(i.span()) for i in re.finditer(L_Bracket, Str)]
            R_Bracket_List = [list(i.span()) for i in re.finditer(R_Bracket, Str)]
            Set_Bracket = copy.deepcopy(L_Bracket_List)
            Stack = []
            for i, m in enumerate(L_Bracket_List[::-1]):
                for j, n in enumerate(R_Bracket_List):
                    if m[0] < n[0] and n[0] not in Stack:
                        Get_Bracket[-i-1][1] = n[0]
                        Stack.append(n[0])
                        break
            Set_Dict_Bracket = [{"location":tuple(i), "level": 0} for i in Set_Bracket]
            for i, m in enumerate(Set_Bracket[::-1]):
                for n in Set_Bracket[-i-2::1]:
                    if n[0]<m[0] and m[1]<n[1]:
                        Set_Dict_Bracket[i]["level"] += -1
            return Set_Dict_Bracket


        #正则替换
        def Regular_Replece(Regular_Dict, Str):
            Pattern_List =[i for i in Dict_Bracket.keys()]
            Set_MatchStr = re.sub(r"|".join(Pattern_List),
                                  lambda x: Dict_Bracket[x.group()][0], Str)
            return Set_MatchStr


        #括号内分解
        def Str_Split_InBracket(Str, Dict_Bracket):
            Bracket_Level_Set = set([i["level"] for i in Dict_Bracket])

            return True


            
        return True
        
