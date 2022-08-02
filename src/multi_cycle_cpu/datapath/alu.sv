`timescale 1ns/1ps

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
            3'b000:
                // add
                result = sum;
            3'b001:
                // subtract
                result = sum;
            3'b010:
                // and
                result = a & b;
            3'b011:
                // or
                result = a | b;
            3'b101:
                // slt
                result = sum[31];
            3'b110:
                 // sll
                result = a << b[4:0];

            3'b100:
                //lui
                result = b;

            default:
                result = 32'bx;
        endcase

endmodule
