import re

class whisk_asm:
    def __init__(self):
        self.progmem = []
        self.datamem = []
        self.varis = {}
        self.labels = {}
    
    def add(self, a, b):
        out = f"""{a} {self.parseValue("$z")} {self.parseValue("?")}
            {self.parseValue("$z")} {b} {self.parseValue("?")}
            {self.parseValue("$z")} {self.parseValue("$z")} {self.parseValue("?")}
            """
        out = self.formatLines(out)
        return out
            
    def inc(self, a):
        out = f"""{self.parseValue("!-1")} {a} {self.parseValue("?")}
            """
        out = self.formatLines(out)
        return out
    
    def dec(self, a):
        out = f"""{self.parseValue("!1")} {a} {self.parseValue("?")}
            """
        out = self.formatLines(out)
        return out
        
    def jmp(self, a):
        out = f"""{self.parseValue("$z")} {self.parseValue("$z")} {a}
            """
        out = self.formatLines(out)
        return out
    
    def cpy(self, a):
        out = f"""{a} {a} {self.parseValue("?")}
            """
        out = self.formatLines(out)
        return out
        
    def print_(self, a):
        out = f"""{a} -1 {self.parseValue("?")}
            """
        out = self.formatLines(out)
        return out
    
    def assign(self, name, val):
        self.varis[name] = float(len(self.datamem))
        self.datamem += [str(val)]
        return float(self.varis[name])
    
    def parseCode(self, inp):
        inp = inp.split("\n")
        inp = [i.split("#")[0] for i in inp]
        inp = [i.lstrip().rstrip() for i in inp if i != "" and not i.isspace()]
        
        return inp
    
    def parseValue(self, val):
        if val[0] == "!":
            return self.parseLiteral(val)
            
        elif val[0] == "$":
            return self.varis[val]
            
        elif val == "?":
            return "?"
        
        elif val[0] == ":":
            return self.labels[val]
            
        else:
            return val
    
    def parseLiteral(self, lit):
        if lit not in list(self.varis.keys()):
            return self.assign(lit, int(lit[1:]))
        else:
            return float(self.varis[lit])
            
    def formatLines(self, lines):
        return re.sub(' +', ' ', lines).lstrip().rstrip().split("\n")
    
    def resolveQs(self):
        for ln, line in enumerate(self.progmem):
            if "?" in line:
                self.progmem[ln] = re.sub("\?", str((ln+1)*3), line)
                
    def combineAndResolveData(self):
        for ln, line in enumerate(self.progmem):
            spl = line.split(" ")
            outline = ""
            for term in spl:
                if re.search(r'(?<=\d)\.0+\b', term):
                    term = str(int(float(term))+len(self.progmem)*3)
                outline += " " + term
                
            self.progmem[ln] = outline.lstrip()
            
        self.datamem = " ".join(self.datamem)
        self.progmem = "\n".join(self.progmem) + "\n"
        return self.progmem + self.datamem
    
    def assemble(self, code):
        code = self.parseCode(code)
        self.assign("$z", 0)
        self.assign("$halt", -1)
        
        for ln, line in enumerate(code):
            terms = line.split()
            if terms[0] == "add":
                self.progmem += self.add(*[self.parseValue(i) for i in terms[1:3]])
                
            elif terms[0] == "inc":
                self.progmem += self.inc(self.parseValue(terms[1]))
                
            elif terms[0] == "dec":
                self.progmem += self.dec(self.parseValue(terms[1]))
                
            elif terms[0] == "jmp":
                self.progmem += self.jmp(self.parseValue(terms[1]))
                
            elif terms[0] == "cpy":
                self.progmem += self.cpy(self.parseValue(terms[2]))
                self.progmem += self.add(*[self.parseValue(i) for i in terms[1:3]])
                
            elif terms[0][0] == ":":
                self.labels[terms[0]] = len(self.progmem)*3
                
            elif terms[0] == "print":
                self.progmem += self.print_(self.parseValue(terms[1]))
            
            elif terms[0] == "s":
                parsedTerms = [self.parseValue(i) for i in terms[1:]]
                self.progmem += [f"{parsedTerms[0]} {parsedTerms[1]} {parsedTerms[2]}"]
            
            elif terms[1] == "=":
                self.assign(terms[0], terms[2])
            
            else:
                raise SyntaxError(f"Unrecognised Command in line {ln+1}! \n >>> {line}")
                
        self.resolveQs()
        return self.combineAndResolveData()
        
        
                


if __name__ == "__main__":
    f = open("input.sla", "r")
    code = f.read()
    f.close()
    asm = whisk_asm()
    assembled = asm.assemble(code)
    print(assembled)
    f = open("output.slq", "w")
    f.write(assembled)
    f.close()
    




















                