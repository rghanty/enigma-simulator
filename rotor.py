
class Rotor:
    def __init__(self, num, reflector, canvas, start_x, start_y, rotor_width, rotor_height):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.num = num
        self.is_reflector = False
        self.canvas = canvas
        self.start_x = start_x
        self.start_y = start_y
        self.rotor_width = rotor_width
        self.rotor_height = rotor_height
        self.square_height = rotor_height / 3
        self.text_items = {}

        if num == "I":
            self.wiring = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
            self.notch = "Q"
        elif num == "II":
            self.wiring = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
            self.notch = "E"
        elif num == "III":
            self.wiring = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
            self.notch = "V"
        elif num == "IV":
            self.wiring = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
            self.notch = "J"
        elif num == "V":
            self.wiring = "VZBRGITYUPSDNHLXAWMJQOFECK"
            self.notch = "Z"
        else:
            self.is_reflector = True
        
        if (not self.is_reflector):
            self.original_wiring = self.wiring

        if reflector == "A":
            self.reflector = "EJMZALYXVBWFCRQUONTSPIKHGD"
        elif reflector == "B":
            self.reflector = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
        elif reflector == "C":
            self.reflector = "FVPJIAOYEDRZXWGCTKUQSBNMHL"

        if not self.is_reflector:
            self.current = self.alphabet[0]

        self.draw()

    def draw(self):
        if (not self.is_reflector):
            x0 = self.start_x
            y0 = self.start_y
            x1 = x0 + self.rotor_width
            y1 = y0 + self.rotor_height

            self.canvas.create_text((x0 + x1) / 2, y0 - 20, text=f"{self.num}", font=('MS Serif', 14), fill='white')
            # Draw the outer rectangle
            
            self.canvas.create_rectangle(x0, y0, x1, y1, outline='#DDDDDD', fill='#555555', width=2)

            # Draw the three squares inside each rectangle
            for j in range(3):
                sq_y0 = y0 + j * self.square_height
                sq_y1 = sq_y0 + self.square_height
                color = '#777777' if j == 1 else '#555555'  # Brighter middle square
                self.canvas.create_rectangle(x0, sq_y0, x1, sq_y1, outline='#DDDDDD', fill=color, width=2)

                # Store the text reference for each square
                text = self.canvas.create_text((x0 + x1) / 2, (sq_y0 + sq_y1) / 2, text='', font=('Helvetica', 14), fill='white')
                self.text_items[j] = text

            self.update_visual()

    def update_visual(self):
        current_pos = self.current
        current_idx = self.alphabet.index(current_pos)
        prev_pos = self.alphabet[current_idx - 1]
        next_pos = self.alphabet[(current_idx + 1) % 26]

        self.canvas.itemconfig(self.text_items[0], text=prev_pos)
        self.canvas.itemconfig(self.text_items[1], text=current_pos)
        self.canvas.itemconfig(self.text_items[2], text=next_pos)

    def advance(self):
        self.wiring = self.wiring[1:] + self.wiring[0]
        self.alphabet = self.alphabet[1:] + self.alphabet[0]
        self.current = self.alphabet[0]
        self.update_visual()
    
    def retreat(self):
        self.wiring = self.wiring[-1] + self.wiring[0:25]
        self.alphabet = self.alphabet[-1] + self.alphabet[0:25]
        self.current = self.alphabet[0]
        self.update_visual()

    def rotor_reset(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.wiring = self.original_wiring
        self.current = self.alphabet[0]
        self.update_visual()

    def get_notch(self):
        return self.notch

    def forward(self, signal):
        if (not self.is_reflector):
            item = self.wiring[signal]
            index = self.alphabet.find(item)
            
            return index

    def backward(self, signal):
        if (not self.is_reflector):
            item = self.alphabet[signal]
            index = self.wiring.find(item)
            return index

    def reflect(self, signal):
        
        item = self.reflector[signal]
        index = self.alphabet.find(item)
        return index