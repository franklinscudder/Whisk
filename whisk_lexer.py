
"""
A lexer using a custom language for OISC subleq computers.

Tom Findlay (findlaytel@gmail.com)
Jul. 2021

$abcd = 4       abcd stores address 4
$abcd = !4      abcd stores the address of const 4 
!4              const literal 4

$abcd <- !4     abcd tracks dynamic addresses with initial value 4
                rhs must be a literal
                    
s a b c         subleq, b <- $b - $a, jump to c if $b <= 0.

:name           begin subroutine declaration

:endsub         end subroutine declaration

~label          label this point in code flow

goto ~label      jump to label ( 0 0 label_addr ) 
 
call :name       call a subroutine

print $abcd     print value $abcd ($abcd -1 ?)

?               refereces current adress + 3 (used for continuing)
                e.g. "s 1 2 ?" will subtract 2 from 1 and never jump
                
"""

class WhiskLexerError(Exception):
    """Class for Lexer exceptions"""
    pass

TOKEN_TYPES = ("subleq", "addr", "literal", "var", "equ", "assign", "subroutine", \
                "endsub", "label", "goto", "call", "print", "continue")


class whiskToken:
    def __init__(self, name, value):
        self.value = value
        self.name = name
        assert name in TOKEN_TYPES
    
    def __str__(self):
        return f"{self.name} type token, value {self.value}"
        

class whiskLexer():
    def __init__(self):
        pass
        
    def fLex(self, filename):
        with open("test.sla", "r") as f:
            lines = f.readlines()
        
        #remove padding, then comments, then blank lines
        lines = [line.lstrip().rstrip() for line in lines if line]
        lines = [line.split("#")[0] for line in lines if line]
        lines = [line for line in lines if line]
        return self.lex(lines)
    
    def lex(self, lines):
        
        tokens = []
        
        n=1
        for line in lines:
            print("line ", n, ": ", line)
            
            words = line.split()
            for word in words:
                word = word.lstrip().rstrip()
                
                if word[0] == "s":  #var
                    tokens.append(whiskToken("subleq", word[1:]))
                elif word[0] in "0123456789":  #addr
                    tokens.append(whiskToken("addr", word))
                elif word[0] == "!":  #literal
                    tokens.append(whiskToken("literal", word[1:]))
                elif word[0] == "$":  #var
                    tokens.append(whiskToken("var", word[1:]))
                elif word[0] == "=":  #static assign
                    tokens.append(whiskToken("equ", None))
                elif word[0] == "<":  #dyn assign
                    tokens.append(whiskToken("assign", None))
                elif word[0] == ":":  #sub/endsub
                    if word[1:] == "endsub":
                        tokens.append(whiskToken("endsub", None))
                    else:
                        tokens.append(whiskToken("subroutine", word[1:]))
                elif word[0] == "~":  #label
                    tokens.append(whiskToken("label", word[1:]))
                elif word == "goto":  #goto
                    tokens.append(whiskToken("goto", None))
                elif word == "call":  #call
                    tokens.append(whiskToken("call", None))
                elif word == "print":   #print
                    tokens.append(whiskToken("print", None))
                elif word == "?": #continue
                    tokens.append(whiskToken("continue", None))
                else:
                    raise WhiskLexerError(f"Unexpected word {word} encountered!")
            n+=1
            
        return tokens

if __name__ == "__main__":
    lexer = whiskLexer()
    
    tokens = lexer.fLex("test.sla")
    [print(t) for t in tokens]
        
        
        
        
        
        
        
        
        
        
        
        
        
        