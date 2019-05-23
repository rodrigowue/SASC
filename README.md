# [SASC] SPICE Automatic Stack Calculator
This tool parses a SPICE description and automatic calculates the stack factor and generates a sized SPICE output.

>python3 sasc.py [Wpmos/Wnmos Ratio] [Input SPICE]

The default Wp/Wn Ratio is 2. Tool generates a node graph and finds Euler Paths to calculate the Stack Factor.
