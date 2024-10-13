# eagle2jlcpcb

This is a simple python tool inspired by https://www.youtube.com/watch?v=y3GviDr0o1s. 

That video shows how to process the BOM and CPL by hand to create the input files for JLCPCB
to use for PCB assembly. This script will take the zip file from EAGLE that contains the
gerber and BOM/CPL and with one command create .xlsx files to input in the flow for PCB assembly.

Right now it assumes 0603 resistors and capacitors, but that can be adjusted manually for now if
you prefer.

## Example Run
```
$ eagle2jlcpcb.py exampleEagleGerber.zip
$ ls
exampleEagleGerber.zip	processedBom.xlsx	processedCpl.xlsx
```

