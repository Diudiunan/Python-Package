
import re

Str = '(sdds(ojod(kj)jjo(kj)kljd(ojo)))'
Osr = [(0, 31), (5, 30), (10, 13), (17, 20), (25, 29)]
t = r'\('
s = r'\)'
List1 = []
List2 = []
print(re.finditer(t, Str))
for i in re.finditer(t, Str):
    List1.append(i.span())
print(List1)
for i in re.finditer(s, Str):
    List2.append(i.span())
print(List2)
LIST1 = [[i[0], i[1]] for i in List1]
LIST2 = List2
Stack = []
for i, m in enumerate(List1[::-1]):
    for j, n in enumerate(List2):
        if m[0] < n[0] and n[0] not in Stack:
            LIST1[-i-1][1] = n[0]
            Stack.append(n[0])
            break
print(LIST1)
Set_Dict_Bracket = [{"location": tuple(i), "level": 0} for i in LIST1]
print(Set_Dict_Bracket)
for i, m in enumerate(LIST1[::-1]):
    for n in LIST1[-i-2::-1]:
        if n[0]<m[0] and m[1]<n[1]:
            Set_Dict_Bracket[-i-1]["level"] += -1
print(Set_Dict_Bracket)
Set_Dict = set([i["level"] for i in Set_Dict_Bracket])
print(Set_Dict)
print(sorted(list(Set_Dict), reverse = False))
STR = Str
for j in sorted(list(Set_Dict), reverse = False):
    for i in Set_Dict_Bracket:
        if i["level"] == j:
            print(Str[i["location"][0]+1:i["location"][1]])
            STR = Str[:i["location"][0]+1]+"TT"+Str[i["location"][1]:]
            print(STR)
print(STR)
