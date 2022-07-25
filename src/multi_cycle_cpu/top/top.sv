///////////////////////////////////////////////////////////////
// top
//
// Instantiates multicycle RISC-V processor and memory
///////////////////////////////////////////////////////////////

`timescale 1ns/1ps

module top(input  logic        clk, reset,
               output logic [31:0] WriteData, DataAdr,
               output logic        MemWrite);

    logic [31:0] ReadData;

    riscvmulti rvmulti(
                   .clk(clk),
                   .reset(reset),
                   .MemWrite(MemWrite),
                   .DataAdr(DataAdr),
                   .WriteData(WriteData),
                   .ReadData(ReadData)
               );


    mem memory(
            .clk(clk),
            .we(MemWrite),
            .a(DataAdr),
            .wd(WriteData),
            .rd(ReadData)
        );
endmodule
