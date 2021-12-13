// file: test5_tb.v
// author: @leithy
// Testbench for test5

`timescale 1ns/1ns

module test5_tb;
	// Declarations
	reg [7:0]  d2;
	reg [7:0]  d1;
	reg  ld2;
	reg  clk;
	reg  ld1;
	wire [7:0]  q2;
	wire [7:0]  q1;
	
	
	 initial begin
        clk = 0;
        forever 
             #(10/2) clk = ~clk;
    end

	// Instantiation of Unit Under Test
	test5 uut (
		.d2(d2),
		.d1(d1),
		.ld2(ld2),
		.clk(clk),
		.ld1(ld1),
		.q2(q2),
		.q1(q1)
	);

	initial begin
		// Input Initialization
		d2 = 1;
		d1 = 5;
		ld2 = 0;
		ld1 = 1;

		// Reset
		#100;
		d2 = 1;
		d1 = 5;
		ld2 = 0;
		ld1 = 1;
		
		
		#100;
		d2 = 10;
		d1 = 5;
		ld2 = 1;
		ld1 = 1;
		
	end

endmodule