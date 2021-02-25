

"""
An assembler using a custom language for OISC subleq computers.

Tom Findlay (findlaytel@gmail.com)
Feb. 2021

$abcd = 4   ## abcd evals to addr(4) ONLY FOR DYNAMICS
!4           ## literal 4 store in data array

:subroutine  ## store entry point? in data array


:endsub  ## goto entry point?

~label   ## writes its address to a byte in data array

goto label   ( 0 0 label_addr )  
call subroutine   store entry point, goto subroutine

s A B C

print $abcd   ## $abcd -1 ?    ## ? = current adress+3

$abcd = !4
vs
$abcd = 4

assignments and literals in loops and subs

"""
class whisk_asm:
    def __init__(self): 
        self.datamem = []
        self.progmem = []
        self.labels = {}
        self.varis = {}
    
    def parseCode(self, inp):
        inp = inp.split("\n")
        inp = [i.lstrip().rstrip() for i in inp if i != "" and not i.isspace()]
        return inp
        
    def assign(self, name, val):
        self.varis[name] = float(len(self.datamem))
        self.datamem += [int(val)]
        return float(self.varis[name])
        
    def parseLiteral(self, lit):
        if lit not in list(self.varis.keys()):
            return self.assign(lit, int(lit[1:]))
        else:
            return float(self.varis[lit])
        
        
        
    def parseValue(self, val):
        if val[0] == "!":
            return self.parseLiteral(val)
            
        elif val[0] == "$":
            return self.varis[val]
            
        elif val == "?":
            return len(self.progmem) + 3
        
        elif val[0] == "~":
            return self.labels[val]
            
        else:
            return int(val)
            
    def expandCalls(self, code):
        subs = {}
        inProc = False
        NProcs = 0
        for line in code:
            #print(line)
            if inProc and line[0] != ":":
                subs[name].append(line)
                #code.remove(line)
            
            elif line[0] == ":":
                if line[:7] != ":endsub":
                    name = line[1:].strip()
                    subs[name] = []
                    inProc = True
                    NProcs += 1
                    #code.remove(line)
                    
                elif line[:7] == ":endsub":
                    inProc = False
                    #code.remove(line)
                    
            
                
        
        for i in range(NProcs):
            start = [line[0] for line in code].index(":")
            stop = [line.rjust(7)[:7] for line in code].index(":endsub")
            
            del code[start:stop+1]
            
        for ln, line in enumerate(code):
            if line[:4] == "call":
                name = line.split(" ")[1].strip()
                code[ln:ln+1] = tuple(subs[name])
                #code.remove(line)
                
        # print(subs)
        # print(code)
        return code  
        
        
    def genLitRestore(self, a, lit):
        return f"s {a} {lit} ?", f"s {a} $Z ?", f"s $Z {lit} ?", "s $Z $Z ?"
        
    def restoreLiterals(self, code):
        #print(code)
        dontUntil0 = 0
        for ln, line in enumerate(code):
            if line[0] == "s" and not dontUntil0:
                line = line.split()
                term1 = line[1].strip()
                term2 = line[2].strip()
                term3 = line[3].strip()
                if  term2[0] == "!":
                    if term3[0] == "~":
                        print(code)
                        lab = code.index(term3)
                    elif term3 != "?":
                        lab = int(term3)
                    else:
                        lab = ln
                    for line in self.genLitRestore(term1, term2):
                        code.insert(lab, line)
                    dontUntil0 = 4
            else:
                dontUntil0 -= 1
        return code
            
    def assignXYZ(self, code):
        code.insert(0, "$Z = 0")
        code.insert(0, "$X = 0")
        code.insert(0, "$Y = 0")
        return code
            
        
    def assemble(self, code):
        code = self.parseCode(code)
        code = self.assignXYZ(code)
        code = self.expandCalls(code)
        code = self.restoreLiterals(code)
        
        print(code)
        
        for line in code:
            #print(line)
            if line[0] == "$":
                line = line.split("=")
                self.assign(line[0].strip(), line[1])
                
            elif line[0] == "s":
                line = line.split(" ")
                self.progmem += [self.parseValue(i) for i in line[1:4]]
                
            elif line[0] == "~":
                line = line.strip()
                self.labels[line] = len(self.progmem)
                
            elif line[:4] == "goto":
                line = line.split()
                self.progmem += [0, 0, self.labels[line[1]]]
                
            elif line[:5] == "print":
                line = line.split(" ")
                self.progmem += [self.parseValue(line[1].strip()), -1, self.parseValue("?")]
        
        offset = len(self.progmem)
        self.progmem = [int(i+(offset*int(type(i) == float))) for i in self.progmem]
        
        out = self.progmem + self.datamem
        
        i = 1
        while i < len(out):
            out.insert(i, ' ')
            i += 2
        
        i = 6
        while i < len(out):
            out.insert(i, '\n')
            i += 7
            
        out = map(str, out)    
        out = ''.join(out)
        
        
        return out
        
inp = """
    $count = 55
    
    
    :print
    print $count
    :endsub
    
    :inc
    s !-1 $count ?
    :endsub
    s $count $count ?
    s !-55 $count ?
    ~here
    call print
    call inc
    s $count !255 ~done
    goto ~here
    ~done
    """

asm = whisk_asm()
assembled = asm.assemble(inp)
f = open("output.slq", "w")
f.write(assembled)
f.close()
    
        
# print(asm.datamem)
# print(asm.progmem)
# print(asm.varis)
# print(asm.labels)
print("Result: ")
print(assembled)