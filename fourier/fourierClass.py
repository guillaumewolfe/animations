from manim import *
import itertools as it
import math
import cmath
import csv

class FourierClass(VGroup):

    def __init__(self,file,*args, **kwargs):
        self.imageFunction = self.csv_to_complex(file)
        VGroup.__init__(self, *args, **kwargs)


    def fourier_transform(self):
        X = []
        N = len(self.imageFunction)
        for k in range(N):
            complexeNumber = 0+0j
            for n in range(N):
                angle = 2*PI*k*n/N
                complexeNumber = math.cos(angle) - math.sin(angle)*1j
                complexeNumber = self.imageFunction[n]*complexeNumber

            newComplexeNumber = complex(complexeNumber.real/N,complexeNumber.imag/N)
            frequence = k
            amplitude = abs(newComplexeNumber)
            phase = cmath.phase(newComplexeNumber)
            X.append([newComplexeNumber.real,newComplexeNumber.imag,frequence,amplitude,phase])
        return X
    
    def csv_to_complex(self,file):
        complex_numbers = []
        
        with open(file, 'r') as file:
            reader = csv.DictReader(file)
            
            # Extract x and y values and create complex numbers
            for row in reader:
                x = float(row['x'])
                y = float(row['y'])
                complex_numbers.append(complex(x, y))
        
        return complex_numbers

            

