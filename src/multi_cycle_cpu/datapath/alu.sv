`timescale 1ns/1ps

`include "alu.vh"

module alu( input  logic [31:0] a, b,
            input  logic [2:0]  alucontrol,
            output logic [31:0] result,
            output logic Z,
            output logic C,
            output logic V,
            output logic N
        );

    logic [31:0] condinvb, sum;
    logic C_out;

    aluflags aluFlags(
                .alucontrol(alucontrol),
                .C_out(C_out),
                .result(result), 
                .sum(sum[31]),
                .a(a[31]),
                .b(b[31]),
                .Z(Z),
                .C(C),
                .V(V),
                .N(N)
    );

    assign condinvb = alucontrol[0] ? ~b : b;
    assign {C_out, sum} = a + condinvb + alucontrol[0];

    always_comb
        case (alucontrol)
            `ALU_ADD:
                result = sum;
            `ALU_SUB:
                result = sum;
            `ALU_AND:
                result = a & b;
            `ALU_OR:
                result = a | b;
            `ALU_SLT:
                result = sum[31];
            `ALU_SLL:
                result = a << b[4:0];

            `ALU_LUI:
                result = b;

            default:
                result = `ALU_DEFAULT;
        endcase

endmodule
