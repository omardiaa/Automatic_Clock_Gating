// file: test4_tb.v
// author: @leithy
// Testbench for test4

`timescale 1ns/1ns

module test4_tb;
	// Declarations
	reg [32:0]  b;
	reg [32:0]  a;
	reg  rst;
	reg  s;
	reg  clk;
	wire [32:0]  x;
  initial begin
        clk = 0;
        forever 
             #(10/2) clk = ~clk;
    end

	// Instantiation of Unit Under Test
	test4 uut (
		.b(b),
		.a(a),
		.rst(rst),
		.s(s),
		.clk(clk),
		.x(x)
	);

	initial begin
		
		rst = 1;
	
		// Reset
		
		#100;
		b = 1;
		a = 2;
		rst = 0;
		s = 1;


		#100;
		b = 1;
		a = 3;
		rst = 0;
		s = 0;
		
		#100 
		rst = 1; 
		
		#100;
		
		b = 1;
		a = 3;
		rst = 0;
		s = 1;
		
		#100;
		
		b = 5;
		a = 3;
		rst = 0;
		s = 1;
		
		
		
	end

endmodule