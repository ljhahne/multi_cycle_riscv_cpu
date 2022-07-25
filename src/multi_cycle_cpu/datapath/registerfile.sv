`timescale 1ns/1ps


module registerfile(input  logic        clk,
                        input  logic        we3,
                        input  logic [ 4:0] a1, a2, a3,
                        input  logic [31:0] wd3,
                        output logic [31:0] rd1, rd2);

    logic [31:0] rf[31:0];

    // three ported register file
    // read two ports combinationally (A1/RD1, A2/RD2)
    // write third port on rising edge of clock (A3/WD3/WE3)
    // register 0 hardwired to 0

    integer i;
    initial begin
        for (i = 0; i < 32; i = i + 1) begin
            rf[i] = 32'b0;

        end
    end


    always_ff @(posedge clk)
              if (we3)
                  rf[a3] <= wd3;

    assign rd1 = (a1 != 0) ? rf[a1] : 0;
    assign rd2 = (a2 != 0) ? rf[a2] : 0;
endmodule
