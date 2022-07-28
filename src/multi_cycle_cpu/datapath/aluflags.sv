`timescale 1ns/1ps


module aluflags(
                input  logic [2:0]  alucontrol,
                input logic C_out,
                input logic[31:0] result, 
                input logic sum,
                input logic a,
                input logic b,
                output logic Z,
                output logic C,
                output logic V,
                output logic N
);


assign Z = (result == 32'b0);
assign C = ~alucontrol[1] & C_out;
assign V = ~(alucontrol[0] ^ a ^ b) & (a ^ sum) & ~alucontrol[0];
assign N = result[31];

endmodule