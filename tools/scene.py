from manim import *
from neural_network_ajust import NeuralNetworkMobject

class neuralNetwork(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        myNetwork = NeuralNetworkMobject(
            [17, 11, 13, 10,3],
            brace_for_large_layers=False,
            edge_propogation_color=LIGHT_GREY,  # Custom color
            output_neuron_color=GREEN_C,      # Custom color
            input_neuron_color=BLUE_D,        # Custom color
            hidden_layer_neuron_color=[PURPLE_A, PINK],
        )
        myNetwork.label_inputs("x")
        myNetwork.label_outputs("y")
        myNetwork.label_outputs_text(["Marcher", "Courir", "Tomber"])
        myNetwork.label_input_text(["Bras Droit","Jambe","Coude","Corp","Bassin","corp","Bras droit","Bras gauche","Hanche","Tibia","Main gauche","Main droite","Pied droit","Pierd gauche","Epaule droite","Epaule gauche","Autre"])
        myNetwork.scale(1)
        myNetwork.label_hidden_layers("h")
        self.play(Write(myNetwork),run_time=5)
        self.wait()
