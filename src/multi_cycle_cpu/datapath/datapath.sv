
`timescale 1ns/1ps


module datapath #(parameter WIDTH = 32)(  input  logic       clk,
            input  logic       reset,
            input logic [2:0] ImmSrc,
            input logic [1:0] ALUSrcA, ALUSrcB,
            input logic [1:0] ResultSrc,
            input logic       AdrSrc,
            input logic [2:0] ALUControl,
            input logic       IRWrite, PCWrite,
            input logic       RegWrite,
            input logic [31:0] ReadData, //Memory
            output logic [31:0] DataAdr, //Memory
            output logic [31:0] WriteData, //Memory
            output logic N,
            output logic Z,
            output logic C,
            output logic V,
            output logic [31:0] Instr
                                           );


    logic [WIDTH-1:0] PC, OldPC, Result, Data, rd1, rd2, A, ImmExt, SrcA, SrcB, ALUResult, ALUOut;

    flopenr #(WIDTH) pcReg(.clk(clk), .reset(reset), .en(PCWrite), .d(Result), .q(PC));


    mux2 #(WIDTH)  pcMux(.d0(PC), .d1(Result), .s(AdrSrc), .y(DataAdr));

    // to external memory

    flop #(WIDTH) dataReg(.clk(clk), .d(ReadData), .q(Data));

    flopenrdual #(WIDTH) instructionReg(
                    .clk(clk),
                    .reset(reset),
                    .en(IRWrite),
                    .d1(ReadData),
                    .d2(PC),
                    .q1(Instr),
                    .q2(OldPC)
                    
                );


    registerfile registerFile(
                     .clk(clk),
                     .we3(RegWrite),
                     .a1(Instr[19:15]),
                     .a2(Instr[24:20]),
                     .a3(Instr[11:7]),
                     .wd3(Result),
                     .rd1(rd1),
                     .rd2(rd2)
                 );

    extend      ext(
                    .instr(Instr[WIDTH-1:7]), 
                    .immsrc(ImmSrc), 
                    .immext(ImmExt)
                );


    flopdual #(WIDTH) rd1rd2Reg(
                 .clk(clk),
                 .d1(rd1),
                 .d2(rd2),
                 .q1(A),
                 .q2(WriteData)
             );

    mux3 #(WIDTH)  SrcAmux(
                        .d0(PC), 
                        .d1(OldPC), 
                        .d2(A), 
                        .s(ALUSrcA), 
                        .y(SrcA)
                    );
    mux3 #(WIDTH)  SrcBmux(
                        .d0(WriteData), 
                        .d1(ImmExt), 
                        .d2(4), 
                        .s(ALUSrcB), 
                        .y(SrcB)
                    );

    alu  alu(
            .a(SrcA), 
            .b(SrcB), 
            .alucontrol(ALUControl), 
            .result(ALUResult), 
            .N(N), 
            .Z(Z), 
            .C(C), 
            .V(V)
        );

    flop #(WIDTH) aluOutReg(
                        .clk(clk), 
                        .d(ALUResult), 
                        .q(ALUOut)
                    );

    mux3 #(WIDTH)  ResultSrcmux(
                            .d0(ALUOut), 
                            .d1(Data), 
                            .d2(ALUResult), 
                            .s(ResultSrc), 
                            .y(Result)
                        );

endmodule


