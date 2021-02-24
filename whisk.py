"""
A OISC emulation using the Subleq operation.

Tom Findlay (findlaytel@gmail.com)

Feb. 2021
"""


class whisk:
    def __init__(self, memory=1000):
        self.memory = [0]*memory
        
    def subleq(self,addr):
        if addr < 0:
            return None
        
        A = self.memory[addr]
        B = self.memory[addr+1]
        C = self.memory[addr+2]
        
        if B == -1:
            print(chr(self.memory[A]), end="")
            return addr+3
            
        else:
            sub = self.memory[B] - self.memory[A]
            self.memory[B] = sub
        
            if sub <= 0:
                return C
        
            return addr+3
    
    def run(self, code):
        code = code.split()
        code = [int(i) for i in code]
        self.memory[0:len(code)] = code
        pc = 0
        
        while pc != None:
            pc = self.subleq(pc)
            
        return True

if __name__ == "__main__":        
    code = """
    12 12 3
    36 37 6
    37 12 9
    37 37 12
    0 -1 15
    38 36 18
    12 12 21
    53 37 24
    37 12 27
    37 37 30
    36 12 -1
    37 37 0
    39 0 -1
    72 101 108
    108 111 44
    32 87 111
    114 108 100
    33 10 53
    """
    w = whisk()
    w.run(code)
    
    