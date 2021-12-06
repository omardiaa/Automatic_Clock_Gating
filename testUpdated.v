

module test2
(
  d1,
  d2,
  clk,
  ld1,
  ld2,
  q1,
  q2
);

  __clockgate_cell__
  (
    .GCLK(__clockgate_output_gclk_),
    .GATE(EN),
    .CLK(CLK)
  )

endmodule

