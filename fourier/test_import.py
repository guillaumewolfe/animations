from fourierClass import FourierClass
from manim import *

test = FourierClass("train.csv")
liste_points = test.fourier_transform()
amp=[]
for i in liste_points:
    amp.append(i["amp"])
print(amp)