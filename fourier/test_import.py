from fourierClass import FourierClass
from manim import *

test = FourierClass("train.csv",10)
liste_points = test.fourier_transform()
liste_points = sorted(liste_points, key=lambda x: x['amp'], reverse=True)
amp=[]
amp2=[]
for index,i in enumerate(liste_points):
        amp.append(i["freq"])
print(amp[:10])