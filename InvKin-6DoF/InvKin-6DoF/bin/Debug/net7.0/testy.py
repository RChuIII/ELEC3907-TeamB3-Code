from pythonnet import load
load("coreclr")

import clr

clr.AddReference("InvKin-6DoF")
from InvKin_6DoF import AngleClac


print(AngleClac.getMathE())
print(AngleClac.getAbs(-10))