

"""
An assembler using a custom language for OISC subleq computers.

Tom Findlay (findlaytel@gmail.com)
Feb. 2021

$abcd = 4   ## abcd evals to addr(4) ONLY FOR DYNAMICS
!4           ## literal 4 store in data array

:subroutine  ## store entry point? in data array


:endsub  ## goto entry point?

~label   ## writes its adress to a byte in data array

goto label   ( 0 0 label_addr )  

A B C

print $abcd   ## 0 -1 ?    ## ? = current adress+3


"""
class whisk_asm:
    def __init__(self): 
        self.datamem = []
        self.progmem = []
        self.varis = {}
    
    def parseCode(self, inp):
        inp = inp.split("\n")
        inp = [i.lstrip().rstrip() for i in inp if i != "" and not i.isspace()]
        return inp
        

    def assemble(self, code):
        code = self.parseCode(code)
        
        for line in code:
            print(line)
            if line[0] == "$":
                line = line.split("=")
                self.varis[line[0]] = len(self.datamem)
                self.datamem += [int(line[1])]
        
inp = """
    $abcd = 4
    3 0 !4
    """

asm = whisk_asm()
asm.assemble(inp) 
    
        
print(asm.datamem)
print(asm.progmem)
print(asm.varis)