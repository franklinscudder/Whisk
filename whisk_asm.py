

"""

$abcd = 4   ## abcd evals to addr(4) ONLY FOR DYNAMICS
!4           ## literal 4 store in data array

:subroutine  ## store entry point? in data array


:endsub  ## goto entry point?

~label   ## writes its adress to a byte in data array

goto label   ( 0 0 label_addr )  

A B C

print $abcd   ## 0 -1 ?    ## ? = current adress+3


"""

datamem = []
progmem = []
varis = {}

inp = """
    $abcd = 4
    3 0 !4
    """
inp = inp.split("\n")
inp = [i.lstrip().rstrip() for i in inp if i != "" and not i.isspace()]

for line in inp:
    print(line)
    if line[0] == "$":
        line = line.split("=")
        varis[line[0]] = len(datamem)
        datamem += [int(line[1])]
    
    
        
print(datamem)
print(progmem)
print(varis)