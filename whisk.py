"""
A OISC emulation using the Subleq operation.

Tom Findlay (findlaytel@gmail.com)

Feb. 2021
"""


class whisk:
    def __init__(self, memory=30000):
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
    f = open("output.slq", "r")
    code = f.read()
    f.close()
    w = whisk()
    w.run(code)
    
    