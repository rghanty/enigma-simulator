class Plugboard:

    def __init__(self, pairs):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.wiring  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.original_wiring = self.wiring
        for pair in pairs:
            A = pair[0]
            B = pair[1]

            pos_A = self.alphabet.find(A)
            pos_B = self.alphabet.find(B)

            self.alphabet = self.alphabet[:pos_A] + B + self.alphabet[pos_A+1:]
            self.alphabet = self.alphabet[:pos_B] + A + self.alphabet[pos_B+1:]
        
    def forward(self, letter):
        index = self.wiring.find(letter)
        item = self.alphabet[index]
        return self.wiring.find(item)
    
    def backward(self, signal):
        item = self.wiring[signal]
        index = self.alphabet.find(item)
        
        return index
    
    def pb_reset(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.wiring = self.original_wiring
    
