// file: test4.v
// author: @leithy

`timescale 1ns/1ns
module test4(input [32:0] a, b, input rst, input s, input clk, output reg [32:0] x);
	

	
	always @(posedge clk)
	
	  if(rst) begin 
	  x <= 0;
	  end 
	  
	  else if(s) begin 
		   x <= a * b;
		end 
		
endmodule
