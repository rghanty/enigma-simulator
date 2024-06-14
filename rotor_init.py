class Rotor:
    def __init__(self, num, reflector):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.num = num
        self.is_reflector = False

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


    def advance(self):
        self.wiring = self.wiring[1:] + self.wiring[0]
        self.alphabet = self.alphabet[1:] + self.alphabet[0]
        self.current = self.alphabet[0]
   
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