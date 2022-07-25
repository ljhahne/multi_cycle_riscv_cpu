`timescale 1ns/1ps

module flopenrdual #(parameter WIDTH = 32)
    (
        input   logic                    clk,
        input   logic                    reset,
        input   logic                    en,
        input   logic   [WIDTH-1:0]     d1,
        input   logic   [WIDTH-1:0]     d2,
        output  logic   [WIDTH-1 :0]    q1,
        output  logic   [WIDTH-1 :0]    q2
    );

    flopenr  #(WIDTH) flopenr1 (
                 .clk(clk),
                 .reset(reset),
                 .en(en),
                 .d(d1),
                 .q(q1)
             );


    flopenr  #(WIDTH) flopenr2 (
                 .clk(clk),
                 .reset(reset),
                 .en(en),
                 .d(d2),
                 .q(q2)
             );


endmodule
