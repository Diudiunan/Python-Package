import json
import re

Str = "sin((x+e**x)*cosx/lnx)"

with open('TRS.json', 'r') as TR:
    p = json.load(TR)
    print(p)
    Targ = [i for i in p.keys()]
    print(Targ)
    Capt = lambda x: p[x.group()][0]
    print(re.sub(r"|".join(Targ), Capt, Str))
    print(re.sub(r"|".join(Targ), lambda x: p[x.group()][0], Str))
