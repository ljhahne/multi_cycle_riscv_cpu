///////////////////////////////////////////////////////////////
// riscvmulti
//
// Multicycle RISC-V microprocessor
///////////////////////////////////////////////////////////////

`timescale 1ns/1ps
`include "riscv.vh"

module riscvmulti #(parameter WIDTH = 32) (
        input   logic         clk,
        input   logic         reset,
        input   logic [WIDTH-1:0] ReadData,
        output  logic         MemWrite,
        output  logic [WIDTH-1:0] DataAdr,
        output  logic [WIDTH-1:0] WriteData
    );

    logic [WIDTH-1:0]   Instr;
    logic [2:0] ALUControl;
    logic [1:0] ALUSrcA, ALUSrcB, ImmSrc, ResultSrc;
    logic PCWrite, RegWrite;
    logic Zero;
    

    controller riscvcontroller(
                   .clk(clk),
                   .reset(reset),
                   .op(opcodetype'(Instr[6:0])),
                   .funct3(Instr[14:12]),
                   .funct7b5(Instr[30]),
                   .Zero(Zero),
                   .ImmSrc(ImmSrc),
                   .ALUSrcA(ALUSrcA),
                   .ALUSrcB(ALUSrcB),
                   .ResultSrc(ResultSrc),
                   .AdrSrc(AdrSrc),
                   .ALUControl(ALUControl),
                   .IRWrite(IRWrite),
                   .PCWrite(PCWrite),
                   .RegWrite(RegWrite),
                   .MemWrite(MemWrite)
               );


    datapath #(WIDTH) dp(
                 .clk(clk),
                 .reset(reset),
                 .ImmSrc(ImmSrc),
                 .ALUSrcA(ALUSrcA),
                 .ALUSrcB(ALUSrcB),
                 .ResultSrc(ResultSrc),
                 .AdrSrc(AdrSrc),
                 .ALUControl(ALUControl),
                 .IRWrite(IRWrite),
                 .PCWrite(PCWrite),
                 .RegWrite(RegWrite),
                 .ReadData(ReadData),
                 .DataAdr(DataAdr),
                 .WriteData(WriteData),
                 .Zero(Zero),
                 .Instr(Instr)
             );

endmodule
