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
        self.circle = Circle(radius=radius,color=LIGHT_PINK).set_stroke(opacity=0.3)
        self.dot = Dot(radius=0.05,color=GREEN_C).move_to(self.circle.get_start())
        self.vector = Line(ORIGIN, self.dot.get_center(), color=BLUE_C)

    def update(self, origin, dt):
        # Update the dot's position
        self.elapsed_time += dt
        proportion = (self.freq * self.elapsed_time + self.phase) % 1
        self.dot.move_to(self.circle.point_from_proportion(proportion))
        # Update the vector's start and end to match the new origin and dot's position
        self.vector.become(Line(origin, self.dot.get_center(), color=BLUE_C,stroke_width=2))
        self.circle.move_to(origin)
        return self.dot.get_center()
fichier = "coordinator.csv"
class CircularMotion(Scene):
    def construct(self):
        self.camera.background_color = DARKER_GRAY
        systems = [
            CircularSystem(1, 0, 0),#Amplitude,frequence,phase
            CircularSystem(0.7, -0.2, 0.2),
            CircularSystem(0.6, 0.8, 0.1),
            CircularSystem(0.5, -1, 0.1),
            CircularSystem(0.4, -0.1, 0.1),
            CircularSystem(0.3, 1.2, 2),
            CircularSystem(0.2, 4,0)]

        for system in systems:
            self.add(system.circle, system.dot, system.vector)

        # The updater function for the group
        def update_systems(mob, dt):
            last_origin = ORIGIN
            for system in systems:
                last_origin = system.update(last_origin, dt)

        # Using always_redraw with a dummy Group to utilize a single updater for all systems
        group = Group(*[s.dot for s in systems], *[s.vector for s in systems],*[s.circle for s in systems]).add_updater(update_systems)
        self.add(group)

        path = TracedPath(systems[-1].dot.get_center, stroke_color=GREEN_C, stroke_width=3.0)
        self.add(path)

        # Play the animation for 10 seconds
        self.wait(15)

        # Remove the updater
        group.remove_updater(update_systems)

"""        maFonction = FourierClass(fichier)
        liste_points = maFonction.fourier_transform()
        frequences=[]
        amplitudes=[]
        phases=[]
        for i in liste_points:
            frequences.append(i[2])
            amplitudes.append(i[3])
            phases.append(i[4])
        systems=[]
        print(amplitudes)
        amplitudes = [amplitude/50 for amplitude in amplitudes]
        for i in range(len(frequences)):
            systems.append(CircularSystem(amplitudes[i],frequences[i],phases[i]))"""