Automatic_glock_gating tool. 

The aim of this project is to work on a gate level netlist and uses clock gating technique to reduce dynamic power, by disabling the clock whenever the load of the D-ff is turned off. 

The approach implemented works by: 
 1. The function loops on all the components and searches for the Flip Flops (using a predefined flip flop name), specific for the library not and not the intermediate level. 
 2. A recursive function is called and it operates as follows:
    1. Takes the output of the flipflop and searches for a component having an input of the same output
    2. Runs recursively to find the input of the next component having the output of the current component
    3. Stops when the output is the same input of the flipflop
    4. Replaces all the components between Feedback of the flipflop and the input of the flip flop with the clock gate. 


How to run:
  1. Specify the test file gate level name in the main function
  2. Run the python program
