import proty
import numpy as np
import matplotlib.pyplot as plt

Str1 = "sin(e**x+ln(4*x**(3*e)+2))"
Str = "(1/x**2)*sin(1/x)"
File = proty.GetR("TRS.json")
Json_Dict = File.GetRules()
Backer = proty.GoBacker(Str, Json_Dict)
Get_Backer = Backer.Regular_Replace()
print(Get_Backer)
x = np.linspace(0, 1, 1000)
plt.plot(x, eval(Get_Backer))
plt.show()
