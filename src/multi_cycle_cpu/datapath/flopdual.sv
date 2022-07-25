`timescale 1ns/1ps

module flopdual #(parameter WIDTH = 32)
    (
        input logic clk,
        input logic [WIDTH-1:0] d1,
        input logic [WIDTH-1:0] d2,
        output logic [WIDTH-1:0] q1,
        output logic [WIDTH-1:0] q2
    );

    flop #(WIDTH) flop1(
             .clk(clk),
             .d(d1),
             .q(q1)
         );

    flop #(WIDTH) flop2(
             .clk(clk),
             .d(d2),
             .q(q2)
         );


endmodule
