class EnigmaMachine:

    def __init__(self, pb, r1, r2, r3, ref):
        self.ref = ref
        self.r1 = r1
        self.r2 = r2
        self.r3 = r3
        self.pb = pb

    def encipher(self, input):
        signal = self.pb.forward(input)
        signal = self.r3.forward(signal)
        signal = self.r2.forward(signal)
        signal = self.r1.forward(signal)
        signal = self.ref.reflect(signal)
        signal = self.r1.backward(signal)
        signal = self.r2.backward(signal)
        signal = self.r3.backward(signal)
        signal = self.pb.backward(signal)
        self.advance_rotors()
        return chr(signal+65)
    
    def advance_rotors(self):
        r3_curr = self.r3.current
        r2_curr = self.r2.current
        self.r3.advance()
        
        if r3_curr == self.r3.get_notch():
            self.r2.advance()
            if r2_curr == self.r2.get_notch():
                self.r1.advance()
    

    

        
      
        
