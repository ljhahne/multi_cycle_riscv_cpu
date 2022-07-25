`timescale 1ns/1ps

module flopenr #(parameter WIDTH = 32)
    (
        input   logic                    clk,
        input   logic                    reset,
        input   logic                    en,
        input   logic   [WIDTH-1:0]     d,
        output  logic   [WIDTH-1 :0]    q
    );

    always_ff @(posedge clk, posedge reset)
        begin
            if(reset) q <= 0;
            else if (en) q <= d;
        end
endmodule
