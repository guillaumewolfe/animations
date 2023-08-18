from fourierClass import FourierClass
from manim import *
import math
from fourierClass import FourierClass

class CircularSystem:
    def __init__(self, radius, frequency, phase):
        self.radius = radius
        self.freq = frequency
        self.phase = phase
        self.elapsed_time = 0
        # Initial positions
        shift_vector=0
        self.circle = Circle(radius=radius,color=LIGHT_PINK).set_stroke(opacity=1).shift(shift_vector).set_stroke(width=0.4)
        self.dot = Dot(radius=0.04,color=GREEN_C).move_to(self.circle.get_start()).shift(shift_vector).set_stroke(opacity=0.8)
        #self.vector = Line(ORIGIN, self.dot.get_center(), color=BLUE_C).shift(shift_vector)
        self.vector = Vector(self.dot.get_center() - ORIGIN,tip_length=0.1, color=BLUE_C,buff=0).shift(shift_vector)

    def update(self, origin, dt):
        # Update the dot's position
        self.elapsed_time += dt
        proportion = (self.freq * self.elapsed_time + self.phase) % 1
        self.dot.move_to(self.circle.point_from_proportion(proportion))
        # Update the vector's start and end to match the new origin and dot's position
        #self.vector.become(Line(origin, self.dot.get_center(), color=BLUE_C,stroke_width=1))
        direction = self.dot.get_center() - origin
        self.vector.become(Vector(direction, color=BLUE_C, stroke_width=1,tip_length=0.1,buff=0).shift(origin))

        self.circle.move_to(origin)
        return self.dot.get_center()
fichier = "train.csv"

def constructeur_system(fichier):
            maFonction = FourierClass(fichier)
            liste_points = maFonction.fourier_transform()
            systems=[]
            for index,i in enumerate(liste_points):
                if index%50==0:
                    systems.append(CircularSystem(i["amp"]/10,i["freq"],i["phase"]))
            return systems
class CircularMotion(Scene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY
        self.system_shift = 0
        systems = [
            CircularSystem(1, 0, 0),#Amplitude,frequence,phase
            CircularSystem(0.7, 1, 3)]
        #systems = constructeur_system(fichier)
        systems[-1].dot.scale(2.5).set_color(YELLOW)
        for system in systems:
            self.add(system.circle, system.dot, system.vector)


        # The updater function for the group
        def update_systems(mob, dt):
            last_origin = ORIGIN+self.system_shift
            for system in systems:
                last_origin = system.update(last_origin, dt)


        # Using always_redraw with a dummy Group to utilize a single updater for all systems
        group = Group(*[s.dot for s in systems], *[s.vector for s in systems],*[s.circle for s in systems]).add_updater(update_systems)
        self.add(group)
        

        path = TracedPath(systems[-1].dot.get_center, stroke_color=PINK, stroke_width=3.0).set_stroke(opacity=0.6)
        self.add(path)

        # Play the animation for 10 seconds
        self.wait(15)

        # Remove the updater
        group.remove_updater(update_systems)

