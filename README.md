# Automatic_Clock_Gating

#PRIORITY TO COMPLETE 

#CHANGE sky130_fd_sc_hd__mux2_1 AND sky130_fd_sc_hd__a21oi_1  

connected to D-flip-flops to clock gates 

clock gate instances are provided in auto_CG.py 









#We now need to replace the sky130_fd_sc_hd__mux2_1, sky130_fd_sc_hd__a21oi_1, and replace them with 
 clock gates

#we also need to trace the components connected to D-flip-flops ex: spm.synthesis.v remove them and, replace them 
#with clock gates 

#after tracing an input to a D-Flip-Flop in spm.synthesis.v 


example given from sky130_fd_sc_hd__dfrtp_2 _570_ 


d <- sky130_fd_sc_hd__o2bb2a_2 _504_ (description: 2-input NAND and 2-input OR into 2-input AND) 
<- 235 and 236 which are both wires 

another example 

sky130_fd_sc_hd__dfrtp_2 _569_ 

d <- sky130_fd_sc_hd__a22o_2 _503_ <-  sky130_fd_sc_hd__o2bb2a_2 _502_ (2-input NAND and 2-input OR into 2-input AND) 

the inputs of the NAND and the OR 
are wires that are used for the first time 

and wires that are out of 

 sky130_fd_sc_hd__o2bb2a_2 cell 


 still can't figure out this arrangment 





behaviour of sky130_fd_sc_hd__o2bb2a



for A & B 


A | B | Output 
0 | 0 |   0 
0 | 1 |   1
1 | 0 |   1
1 | 1 |   0 

same behaviour as XOR gate 


behaviour of sky130_fd_sc_hd__a22o_2 

X = ((A1 & A2) | (B1 & B2))

A | B | Output 
0 | 0 |   0 
0 | 1 |   0
1 | 0 |   0
1 | 1 |   1 

