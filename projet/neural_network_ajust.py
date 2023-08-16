from manim import *
import itertools as it

# A customizable Sequential Neural Network
class NeuralNetworkMobject(VGroup):
    neuron_radius = 0.15
    neuron_to_neuron_buff = MED_SMALL_BUFF
    layer_to_layer_buff = LARGE_BUFF
    output_neuron_color = WHITE
    input_neuron_color = WHITE
    hidden_layer_neuron_color = WHITE
    neuron_stroke_width = 2
    neuron_fill_color = GREEN
    edge_color = LIGHT_GREY
    edge_stroke_width = 2
    edge_propogation_color = YELLOW
    edge_propogation_time = 200
    max_shown_neurons = 16
    brace_for_large_layers = True
    average_shown_activation_of_large_layer = True
    include_output_labels = False
    arrow = False
    arrow_tip_size = 0.1
    left_size = 1
    neuron_fill_opacity = 1
    add_titles_doted_lines = True
    # Constructor with parameters of the neurons in a list
    def __init__(self, neural_network, *args, **kwargs):
        self.layer_sizes = neural_network
        self.brace_for_large_layers = kwargs.pop('brace_for_large_layers', NeuralNetworkMobject.brace_for_large_layers)
        self.layer_to_layer_buff = kwargs.pop('largeur_layers'*LARGE_BUFF, NeuralNetworkMobject.layer_to_layer_buff)
        self.add_titles_doted_lines = kwargs.pop('titles', NeuralNetworkMobject.add_titles_doted_lines)

        #colors
        self.edge_propogation_color = kwargs.pop('edge_propogation_color', YELLOW)
        self.output_neuron_color = kwargs.pop('output_neuron_color', WHITE)
        self.input_neuron_color = kwargs.pop('input_neuron_color', WHITE)
        self.hidden_layer_neuron_color = kwargs.pop('hidden_layer_neuron_color', WHITE)


        self.adjust_spacings()
        VGroup.__init__(self, *args, **kwargs)
        self.add_neurons()
        self.add_edges()
        self.add_to_back(self.layers)
        if self.add_titles_doted_lines : self.add_layer_labels()
        #self.center_neural_network()

    def center_neural_network(self):
        total_height = self.get_height()
        frame_center = config.frame_height / 2.0
        vertical_shift = frame_center - self.get_center()[1]
        self.shift(DOWN * vertical_shift)
            #Optionnal settings:
    # Helper method for constructor
    def add_neurons(self):
        layers = VGroup(*[
            self.get_layer(size, index)
            for index, size in enumerate(self.layer_sizes)
        ])
        # Adjusting the buff value
        layers.arrange_submobjects(RIGHT, buff=self.layer_to_layer_buff)
        self.layers = layers
        if self.include_output_labels:
            self.label_outputs_text()
    # Helper method for constructor
    def get_nn_fill_color(self, index):
        if index == -1 or index == len(self.layer_sizes) - 1:
            return self.output_neuron_color
        if index == 0:
            return self.input_neuron_color
        else:
            gradient = color_gradient(self.hidden_layer_neuron_color, len(self.layer_sizes) - 2)
            return gradient[index - 1]
    # Helper method for constructor
    def get_layer(self, size, index=-1):
        layer = VGroup()
        n_neurons = size
        if n_neurons > self.max_shown_neurons:
            n_neurons = self.max_shown_neurons
        neurons = VGroup(*[
            Circle(
                radius=self.neuron_radius,
                stroke_color=self.get_nn_fill_color(index),
                stroke_width=self.neuron_stroke_width,
                fill_color=BLACK,
                fill_opacity=self.neuron_fill_opacity,
            )
            for x in range(n_neurons)
        ])
        neurons.arrange_submobjects(
            DOWN, buff=self.neuron_to_neuron_buff
        )
        for neuron in neurons:
            neuron.edges_in = VGroup()
            neuron.edges_out = VGroup()
        layer.neurons = neurons
        layer.add(neurons)

        if size > n_neurons:
            dots = MathTex("\\vdots")
            dots.move_to(neurons)
            VGroup(*neurons[:len(neurons) // 2]).next_to(
                dots, UP, MED_SMALL_BUFF
            )
            VGroup(*neurons[len(neurons) // 2:]).next_to(
                dots, DOWN, MED_SMALL_BUFF
            )
            layer.dots = dots
            layer.add(dots)
            if self.brace_for_large_layers:
                brace = Brace(layer, LEFT*2)
                brace_label = brace.get_tex(str(size))
                layer.brace = brace
                layer.brace_label = brace_label
                layer.add(brace, brace_label)

        return layer
    # Helper method for constructor
    def add_edges(self):
        self.edge_groups = VGroup()
        for l1, l2 in zip(self.layers[:-1], self.layers[1:]):
            edge_group = VGroup()
            for n1, n2 in it.product(l1.neurons, l2.neurons):
                edge = self.get_edge(n1, n2)
                edge_group.add(edge)
                n1.edges_out.add(edge)
                n2.edges_in.add(edge)
            self.edge_groups.add(edge_group)
        self.add_to_back(self.edge_groups)
    # Helper method for constructor
    def get_edge(self, neuron1, neuron2):
        if self.arrow:
            return Arrow(
                neuron1.get_center(),
                neuron2.get_center(),
                buff=self.neuron_radius,
                stroke_color=self.edge_color,
                stroke_width=self.edge_stroke_width,
                tip_length=self.arrow_tip_size
            )
        return Line(
            neuron1.get_center(),
            neuron2.get_center(),
            buff=self.neuron_radius,
            stroke_color=self.edge_color,
            stroke_width=self.edge_stroke_width,
        )
    
    # Labels each input neuron with a char l or a LaTeX character
    def label_inputs(self, l):
        self.output_labels = VGroup()
        if len(l)==1:
            for n, neuron in enumerate(self.layers[0].neurons):
                label = MathTex(f"{l}_"+"{"+f"{n + 1}"+"}")
                label.set_height(0.3 * neuron.get_height())
                label.move_to(neuron)
                self.output_labels.add(label)
        elif len(l) == self.layer_sizes[0]:
            for i, item in enumerate(l):
                neuron = self.layers[0].neurons[i]
                label = MathTex(f"{item}")
                label.set_height(0.3 * neuron.get_height())
                label.move_to(neuron)
                self.output_labels.add(label)
        else:
            raise ValueError(f"The list INPUT length {len(l)} is not equal to the first layer size {self.layer_sizes[0]}.")

        self.add(self.output_labels)

    # Labels each output neuron with a char l or a LaTeX character
    def label_outputs(self, l):
        self.output_labels = VGroup()
        for n, neuron in enumerate(self.layers[-1].neurons):
            label = MathTex(f"{l}_"+"{"+f"{n + 1}"+"}")
            label.set_height(0.4 * neuron.get_height())
            label.move_to(neuron)
            self.output_labels.add(label)
        self.add(self.output_labels)

    # Labels each neuron in the output layer with text according to an output list
    def label_outputs_text(self, outputs):
        self.output_labels = VGroup()
        if len(outputs)!=self.layer_sizes[-1]:
            raise ValueError(f"The list OUTPUT length {len(outputs)} is not equal to the first layer size {self.layer_sizes[-1]}.")
        for n, neuron in enumerate(self.layers[-1].neurons):
            label = MathTex(outputs[n])
            label.set_height(0.75*neuron.get_height())
            label.move_to(neuron)
            label.shift((neuron.get_width() + label.get_width()/2)*RIGHT)
            self.output_labels.add(label)
        self.add(self.output_labels)

    def label_input_text(self, inputs):
        self.input_labels = VGroup()
        if len(inputs) != self.layer_sizes[0]:
            raise ValueError(f"The list INPUT length {len(inputs)} is not equal to the first layer size {self.layer_sizes[0]}.")
        for n, neuron in enumerate(self.layers[0].neurons):
            label = MathTex(inputs[n])
            label.set_height(0.75 * neuron.get_height())
            label.move_to(neuron)
            label.shift((neuron.get_width() + label.get_width() / 2) * LEFT)  # Change to LEFT for inputs
            self.input_labels.add(label)
        self.add(self.input_labels)


    # Labels the hidden layers with a char l or a LaTeX character
    def label_hidden_layers(self, l):
        self.output_labels = VGroup()
        for layer in self.layers[1:-1]:
            for n, neuron in enumerate(layer.neurons):
                label = MathTex(f"{l}_{{{n + 1}}}")
                label.set_height(0.4 * neuron.get_height())
                label.move_to(neuron)
                self.output_labels.add(label)
        self.add(self.output_labels)

    def adjust_spacings(self):
        SCALING = 0.7
        # Get the number of neurons in the largest layer (in terms of visual size)
        max_layer_size = max(self.layer_sizes)
        if max_layer_size > self.max_shown_neurons:
            max_layer_size = self.max_shown_neurons

        # Get the frame height and width from the default camera configuration
        frame_height = config.frame_height
        frame_width = config.frame_width
        
        target_network_height = SCALING * frame_height  # adjust the 0.8 as per requirement
        target_network_width = SCALING * frame_width  # adjust the 0.8 as per requirement

        # Adjust the neuron_radius based on the target network height
        total_buff_space = self.neuron_to_neuron_buff * (max_layer_size - 1)
        available_space_for_neurons = target_network_height - total_buff_space
        self.neuron_radius = 1.7*available_space_for_neurons /(2*max_layer_size)

        # Re-adjust neuron_to_neuron_buff based on the adjusted neuron_radius
        self.neuron_to_neuron_buff = target_network_height / max_layer_size - 2 * self.neuron_radius

        # Adjust layer_to_layer_buff based on target network width and number of layers
        total_layer_width_without_buff = len(self.layer_sizes) * 2 * self.neuron_radius
        extra_space_for_labels = 2  # Adjust this as needed
        total_buff_width = target_network_width - total_layer_width_without_buff - extra_space_for_labels

        self.layer_to_layer_buff = total_buff_width / (len(self.layer_sizes) - 1)
    def add_layer_labels(self):
        layer_names = []

        # For the first layer
        layer_names.append(Text("Entrée").scale(0.7))

        # For the hidden layers
        if len(self.layers) > 2:
            layer_names.append(Text("Couches Cachées").scale(0.7))
            
        # For the last layer
        layer_names.append(Text("Sorties").scale(0.7))
        
        # Determine the y-coordinate of the highest neuron for uniform height of labels
        top_y = max([layer.get_top()[1] for layer in self.layers]) + 1.5 * MED_SMALL_BUFF  # 1.5 times the buffer for aesthetic spacing

        # Position the input label
        layer_names[0].next_to(self.layers[0], UP, buff=MED_SMALL_BUFF)
        layer_names[0].set_y(top_y)

        # Position the hidden layers label if there are hidden layers
        if len(layer_names) > 2:
            # This will place the "Hidden Layers" text between the first and last hidden layers
            first_hidden_layer = self.layers[1]
            last_hidden_layer = self.layers[-2]
            middle_point = (first_hidden_layer.get_center() + last_hidden_layer.get_center()) / 2
            layer_names[1].move_to(middle_point)
            layer_names[1].set_y(top_y)

        # Position the output label
        layer_names[-1].next_to(self.layers[-1], UP, buff=MED_SMALL_BUFF)
        layer_names[-1].set_y(top_y)

        for name in layer_names:
            self.add(name)
        # Determine the maximum height across all layers



        # DOTTED LINES
        max_height = max([layer.get_height() for layer in self.layers])

        # Create the dotted line
        def create_dotted_line():
            return DashedLine(
                start=[0, -max_height/2, 0],
                end=[0, max_height/2, 0]
            )

        # Position the line between the input and first hidden layer
        input_layer = self.layers[0]
        first_hidden_layer = self.layers[1]
        line1_center_x = (input_layer.get_right()[0] + first_hidden_layer.get_left()[0]) / 2
        line1 = create_dotted_line()
        line1.move_to([line1_center_x, self.layers[0].get_center()[1], 0])  # Use the center y-coordinate of the input layer

        # Position the line between the output and the last hidden layer
        output_layer = self.layers[-1]
        last_hidden_layer = self.layers[-2]
        line2_center_x = (output_layer.get_left()[0] + last_hidden_layer.get_right()[0]) / 2
        line2 = create_dotted_line()
        line2.move_to([line2_center_x, self.layers[-1].get_center()[1], 0])  # Use the center y-coordinate of the output layer

        # Add lines to the neural network group
        self.add(line1, line2)
