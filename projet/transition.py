from manim import *
from neural_network_ajust import NeuralNetworkMobject

class nnTransition(Scene):


    def construct(self):
        self.camera.background_color = DARKER_GRAY
        # Initial neural network
        nn1 = NeuralNetworkMobject(
            [17,3],
            brace_for_large_layers=False,
            edge_propogation_color=LIGHT_GREY,  # Custom color
            output_neuron_color=GREEN_C,      # Custom color
            input_neuron_color=BLUE_D,        # Custom color
            hidden_layer_neuron_color=[PURPLE_A, PINK],
        )
        nn1.label_inputs("x")
        nn1.label_outputs("y")
        nn1.label_outputs_text(["Marcher", "Courir", "Tomber"])
        nn1.label_input_text(["Bras Droit","Jambe","Coude","Corp","Bassin","corp","Bras droit","Bras gauche","Hanche","Tibia","Main gauche","Main droite","Pied droit","Pierd gauche","Epaule droite","Epaule gauche","Autre"])
        nn1.scale(1)
        nn1.label_hidden_layers("h")
        nn2 = NeuralNetworkMobject(
            [17, 11, 13, 10,3],
            brace_for_large_layers=False,
            edge_propogation_color=LIGHT_GREY,  # Custom color
            output_neuron_color=GREEN_C,      # Custom color
            input_neuron_color=BLUE_D,        # Custom color
            hidden_layer_neuron_color=[PURPLE_A, PINK],
        )
        nn2.label_inputs("x")
        nn2.label_outputs("y")
        nn2.label_outputs_text(["Marcher", "Courir", "Tomber"])
        nn2.label_input_text(["Bras Droit","Jambe","Coude","Corp","Bassin","corp","Bras droit","Bras gauche","Hanche","Tibia","Main gauche","Main droite","Pied droit","Pierd gauche","Epaule droite","Epaule gauche","Autre"])
        nn2.scale(1)
        nn2.label_hidden_layers("h")
        

        # Display the initial state
        self.play(Write(nn1))

        # Transition to the final state
        self.play(TransformMatchingShapes(nn1,nn2), run_time=3)
        self.wait(3)
    