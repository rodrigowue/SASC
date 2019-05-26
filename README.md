# [SASC] SPICE Automatic Stack Calculator
This tool parses a SPICE description and turns them into a transistor object list, one list for Pull-Down Network (PDN) and one for Pull-Up Network (PUN). A node graph is generated and them the tool finds Eulerian Paths to calculate the Stack Factor and properly size transistor widths. 

>python3 sasc.py [Wpmos/Wnmos Ratio] [Input SPICE]

The default value for "Wp/Wn Ratio" is 2. 

Spice Description should contain a section describing i/o and supply pins. 

>*.pininfo A:I B:I OUT:O VSS:G VDD:P

Where ":I" stands for Inputs, ":O" for outputs, ":G" for Ground, and ":P" for Power.
