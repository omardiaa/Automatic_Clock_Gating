/* Generated by Yosys 0.11 (git sha1 UNKNOWN, clang 13.0.0 -fPIC -Os) */

module test2(d1, d2, clk, ld1, ld2, q1, q2);
  wire _0_;
  wire _1_;
  input clk;
  input d1;
  input d2;
  input ld1;
  input ld2;
  output q1;
  output q2;
  sky130_fd_sc_hd__mux2_1 _2_ (
    .A0(q1),
    .A1(d1),
    .S(ld1),
    .X(_0_)
  );
  sky130_fd_sc_hd__mux2_1 _3_ (
    .A0(q2),
    .A1(d2),
    .S(ld2),
    .X(_1_)
  );
  sky130_fd_sc_hd__dfxtp_1 _4_ (
    .CLK(clk),
    .D(_0_),
    .Q(q1)
  );
  sky130_fd_sc_hd__dfxtp_1 _5_ (
    .CLK(clk),
    .D(_1_),
    .Q(q2)
  );
endmodule