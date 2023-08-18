from manim import *
import itertools as it
import math
import cmath
import csv

class FourierClass(VGroup):

    def __init__(self,file,index=1,*args, **kwargs):
        VGroup.__init__(self, *args, **kwargs)
        self.index=index
        self.x = self.csv_to_complex(file)
        


    def fourier_transform(self):
        X = []
        N = len(self.x)
        for k in range(N):
            sum_complex = 0 + 0j  # Initialize complex sum
            
            for n in range(N):
                angle = (2 * PI * k * n) / N
                c = complex(math.cos(angle),-math.sin(angle))
                sum_complex += self.x[n] * c  # Add the product to the sum

            # Scale the real and imaginary parts by 1/N
            sum_complex = complex(sum_complex.real / N, sum_complex.imag / N)

            frequence = k
            amplitude = abs(sum_complex)  
            phase = cmath.phase(sum_complex)
            X.append({'real': sum_complex.real,'imag': sum_complex.imag,'freq': frequence,'amp': amplitude,'phase': phase})
        return X
    
    def csv_to_complex(self,file):
        complex_numbers = []
        
        with open(file, 'r') as file:
            reader = csv.DictReader(file)
            
            # Extract x and y values and create complex numbers
            for i,row in enumerate(reader):
                if i%self.index==0:
                    x = float(row['x'])
                    y = float(row['y'])
                    complex_numbers.append(complex(x, y))
        
        return complex_numbers

            

