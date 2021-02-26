# Whisk
 A Python OISC emulator and assembler using Subleq
 
Usage
===========
whisk_asm_2.py reads the assembly source file input.sla and writes the assembled
output to output.slq.

whisk.py can the be run which will read the source in output.slq and run it.

Assembly Syntax
====================

I created my own assembly syntax for this project using various conventions
from different places. The following is a list of commands that can be used:

- ```s a b c``` is the standard subleq operation. The value at ```a``` is subtracted
from the value at ```b``` and stored at ```b```. If this value is less than
or equal to zero, the code will branch to adress ```c```. ```b```
can be an adress (```15```) or a variable (```$name```). ```c``` can also be a
label (```:here```) and ```a``` can also be a label or literal (```!42```).
- ```add a b ``` will add the value at a to that at b. The arguments can be
addresses or variables, and ```a``` can be a literal.
- ```inc a``` or ```dec a``` will increment or decrement the value at ```a```.
- ```jmp a``` will jump to the address or label ```a```.
- ```cpy a b``` will copy the value at ```a``` to ```b```.
- ```:here``` declares a label that can be jumped to later.
- ```print a``` prints the value at a to console.
- ```$name = a``` assigns the value ```a``` to the variable with name ```$name```.

Notes
============
- A general rule here is that you can never have a literal as the second argument
to a statement as this will change the stored value of that literal and is
therefore not allowed.
- The symbol ```?``` can be used to specify a jump to the next command with an 
```s``` statement meaning no conditional branching will occur, e.g. ```s !10 $value ?```.

Happy Coding!