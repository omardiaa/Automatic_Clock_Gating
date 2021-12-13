// file: test3.v
// author: @leithy

`timescale 1ns/1ns



module test3(input [16:0] a, b, input rst, input s, input clk, output reg [16:0] x);
	

	
	always @(posedge clk or rst)
	
	  if(rst) begin 
	  x <= 0;
	  end 
	  
	  else if(s) begin 
		   x <= a + b;
		end 
		
endmodule
