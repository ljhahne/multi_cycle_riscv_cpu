
`timescale 1ns/1ps
`include "riscv.vh"


module controller(
                    input  logic       clk,
                    input  logic       reset,
                    input  opcodetype  op,
                    input  logic [2:0] funct3,
                    input  logic       funct7b5,
                    input logic N,
                    input logic Z,
                    input logic C,
                    input logic V,
                    output logic [2:0] ImmSrc,
                    output logic [1:0] ALUSrcA,
                    output logic [1:0] ALUSrcB,
                    output logic [1:0] ResultSrc,
                    output logic       AdrSrc,
                    output logic [2:0] ALUControl,
                    output logic       IRWrite,
                    output logic       PCWrite,
                    output logic       RegWrite,
                    output logic       MemWrite
                    );




    statetype state, state_next;
    wire[1:0] aluOP;
    wire Branch;
    wire PCUpdate;

    controller_fsm controllerFSM(   clk,
                                    reset,
                                    op,
                                    ALUSrcA, ALUSrcB,
                                    ResultSrc,
                                    AdrSrc,
                                    IRWrite,
                                    RegWrite, MemWrite,
                                    aluOP,
                                    Branch,
                                    PCUpdate
                                );



    //ALUOP output from FSM
    alu_decoder aluDecoder( op[5],
                            funct3,
                            funct7b5,
                            aluOP,
                            ALUControl
                          );

    //Instruction Decoder
    instruction_decoder instructonDecoder(op, ImmSrc);

    pc_write pcWrite( .N(N), 
                      .Z(Z), 
                      .C(C), 
                      .V(V), 
                      .funct3(funct3), 
                      .Branch(Branch), 
                      .PCUpdate(PCUpdate),
                      .PCWrite(PCWrite)
                    );


endmodule



