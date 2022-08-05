`timescale 1ns/1ps

`include "alu.vh"

module alu_decoder(   input  logic       opb5,
                          input  logic [2:0] funct3,
                          input  logic       funct7b5,
                          input  logic [1:0] ALUOp,
                          output logic [2:0] ALUControl);

    logic  RtypeSub;
    assign RtypeSub = funct7b5 & opb5;  // TRUE for R-type subtract instruction

    always_comb
        case(ALUOp)
            2'b00:
                ALUControl = `ALU_ADD;
            2'b01:
                ALUControl = `ALU_SUB;
            2'b10:
            case(funct3) // R-type or I-type ALU
                3'b000:
                    if (RtypeSub)
                        ALUControl = `ALU_SUB;
                    else
                        ALUControl = `ALU_ADD;

                3'b001:
                    ALUControl = `ALU_SLL;
                3'b010:
                    ALUControl = `ALU_SLT; // slt, slti
                3'b110:
                    ALUControl = `ALU_OR; // or, ori
                3'b111:
                    ALUControl = `ALU_AND; // and, andi
                default:
                    ALUControl = 3'bxxx; // ??
            endcase

             2'b11:
                ALUControl = `ALU_LUI; //lui

            default:
                ALUControl = 3'bxxx; // ???
        endcase
    endmodule
