

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


  sky130_fd_sc_hd__dlclkp
  __clockgate_cell__
  (
    .GCLK(_0_),
    .GATE(ld1),
    .CLK(clk)
  );


  sky130_fd_sc_hd__dfxtp_1
  _4_
  (
    .CLK(_0_),
    .D(d1),
    .Q(q1)
  );


  sky130_fd_sc_hd__dlclkp
  __clockgate_cell__
  (
    .GCLK(_1_),
    .GATE(ld2),
    .CLK(clk)
  );


  sky130_fd_sc_hd__dfxtp_1
  _5_
  (
    .CLK(_1_),
    .D(d2),
    .Q(q2)
  );


endmodule

