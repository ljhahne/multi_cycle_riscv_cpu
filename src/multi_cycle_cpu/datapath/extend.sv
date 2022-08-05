`timescale 1ns/1ps

`include "immsrc.vh"

module extend(input  logic [31:7] instr,
                  input  logic [2:0]  immsrc,
                  output logic [31:0] immext);

    always_comb
        case(immsrc)
            `IMMSRC_I:
                immext = {{20{instr[31]}}, instr[31:20]};
            // S-type (stores)
            `IMMSRC_S:
                immext = {{20{instr[31]}}, instr[31:25], instr[11:7]};
            // B-type (branches)
            `IMMSRC_B:
                immext = {{20{instr[31]}}, instr[7], instr[30:25], instr[11:8], 1'b0};
            // J-type (jal)
            `IMMSRC_J:
                immext = {{12{instr[31]}}, instr[19:12], instr[20], instr[30:21], 1'b0};

            `IMMSRC_U:
                immext = {instr[31:12], {12{1'b0}}};

            default:
                immext = 32'bx; // undefined
        endcase
    endmodule
