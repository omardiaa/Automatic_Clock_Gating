// file: test5.v
// author: @leithy

`timescale 1ns/1ns

module test5(input [7:0] d1, d2, input clk, ld1, ld2, output reg [7:0] q1, q2);
    
    always @(posedge clk)
    begin
        begin
            if(ld1)
                q1<=d1+d2;
        end


    end
        always @(posedge clk)
    begin

        begin
            if(ld2)
                q2<=d2-d1;
        end

    end
            
endmodule