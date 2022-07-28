`timescale 1ns/1ps

module pc_write(    

                    input logic N,
                    input logic Z,
                    input logic C,
                    input logic V,
                    input  logic [2:0] funct3,
                    input logic Branch,
                    input logic PCUpdate,
                    output logic PCWrite
                   );

    //logic which indicates a branch by alu signals and funct3 bits
    logic branch_funct3;

    //branch logic : beq + bne + blt + bge + bltu + bgeu
    assign branch_funct3 =  ~funct3[2] & ~funct3[1] & ~funct3[0] & Z |
                            ~funct3[2] & ~funct3[1] & funct3[0] & ~Z |
                            funct3[2] & ~funct3[1] & ~funct3[0] & (N | V) |
                            funct3[2] & ~funct3[1] & funct3[0] & ~(N | V) |
                            funct3[2] & funct3[1] & ~funct3[0] & ~C |
                            funct3[2] & funct3[1] & funct3[0] & C;


    assign PCWrite = (branch_funct3 & Branch) | PCUpdate;
endmodule
