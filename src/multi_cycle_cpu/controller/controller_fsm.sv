`timescale 1ns/1ps
`include "riscv.vh"
`include "fsm.vh"

module state_register(input logic clk, input logic reset, input statetype state_next, output statetype state);
    always_ff@(posedge clk, posedge reset)
             if(reset)
                 state <= S_FETCH;
    else
        state <= state_next;

endmodule

module output_logic(input  statetype   state,
                        output logic [1:0] ALUSrcA,
                        output logic [1:0] ALUSrcB,
                        output logic [1:0] ResultSrc,
                        output logic       AdrSrc,
                        output logic       IRWrite,
                        output logic       RegWrite,
                        output logic       MemWrite,
                        output logic [1:0] aluOP,
                        output logic       Branch,
                        output logic       PCUpdate);


    always_comb
        begin
            case(state)
                S_FETCH :
                begin
                    ALUSrcA = `FETCH_ALUSRCA;
                    ALUSrcB = `FETCH_ALUSRCB;
                    ResultSrc = `FETCH_RESULTSRC;
                    AdrSrc = `FETCH_ADRSRC;
                    IRWrite = `FETCH_IRWRITE;
                    aluOP = `FETCH_ALUOP;
                    PCUpdate = `FETCH_PCUPDATE;

                    RegWrite = `DEFAULT_REGWRITE;
                    MemWrite = `DEFAULT_MEMWRITE;
                    Branch = `DEFAULT_BRANCH;

                end

                S_DECODE :
                begin
                    ALUSrcA = `DECODE_ALUSRCA;
                    ALUSrcB = `DECODE_ALUSRCB;
                    aluOP = `DECODE_ALUOP;

                    ResultSrc = `DEFAULT_RESULTSRC;
                    AdrSrc = `DEFAULT_ADRSRC;
                    IRWrite = `DEFAULT_IRWRITE;
                    RegWrite = `DEFAULT_REGWRITE;
                    MemWrite = `DEFAULT_MEMWRITE;
                    Branch = `DEFAULT_BRANCH;
                    PCUpdate = `DEFAULT_PCUPDATE;

                end

                S_MEMADR :
                begin
                    ALUSrcA = `MEMADR_ALUSRCA;
                    ALUSrcB = `MEMADR_ALUSRCB;
                    aluOP = `MEMADR_ALUOP;

                    ResultSrc = `DEFAULT_RESULTSRC;
                    AdrSrc = `DEFAULT_ADRSRC;
                    IRWrite = `DEFAULT_IRWRITE;
                    RegWrite = `DEFAULT_REGWRITE;
                    MemWrite = `DEFAULT_MEMWRITE;
                    Branch = `DEFAULT_BRANCH;
                    PCUpdate = `DEFAULT_PCUPDATE;

                end

                S_EXECUTER :
                begin
                    ALUSrcA = `EXECUTER_ALUSRCA;
                    ALUSrcB = `EXECUTER_ALUSRCB;
                    aluOP = `EXECUTER_ALUOP;

                    ResultSrc = `DEFAULT_RESULTSRC;
                    AdrSrc = `DEFAULT_ADRSRC;
                    IRWrite = `DEFAULT_IRWRITE;
                    RegWrite = `DEFAULT_REGWRITE;
                    MemWrite = `DEFAULT_MEMWRITE;
                    Branch = `DEFAULT_BRANCH;
                    PCUpdate = `DEFAULT_PCUPDATE;

                end

                S_EXECUTEL :
                begin
                    ALUSrcA = 2'b10;
                    ALUSrcB = 2'b01;
                    aluOP = 2'b10;

                    ResultSrc = 2'b00;
                    AdrSrc = 1'b0;
                    IRWrite = 1'b0;
                    RegWrite = 1'b0;
                    MemWrite = 1'b0;
                    Branch = 1'b0;
                    PCUpdate = 1'b0;

                end

                S_JAL :
                begin
                    ALUSrcA = 2'b01;
                    ALUSrcB = 2'b10;
                    ResultSrc = 2'b00;
                    aluOP = 2'b00;
                    PCUpdate = 1'b1;

                    AdrSrc = 1'b0;
                    IRWrite = 1'b0;
                    RegWrite = 1'b0;
                    MemWrite = 1'b0;
                    Branch = 1'b0;

                end

                S_BEQ :
                begin
                    ALUSrcA = 2'b10;
                    ALUSrcB = 2'b00;
                    aluOP = 2'b01;
                    ResultSrc = 2'b00;
                    Branch = 1'b1;

                    AdrSrc = 1'b0;
                    IRWrite = 1'b0;
                    RegWrite = 1'b0;
                    MemWrite = 1'b0;
                    PCUpdate = 1'b0;

                end

                S_MEMREAD :
                begin
                    ResultSrc = 2'b00;
                    AdrSrc = 1'b1;

                    ALUSrcA = 2'b00;
                    ALUSrcB = 2'b00;
                    IRWrite = 1'b0;
                    RegWrite = 1'b0;
                    MemWrite = 1'b0;
                    aluOP = 2'b00;
                    Branch = 1'b0;
                    PCUpdate = 1'b0;

                end

                S_MEMWRITE :
                begin
                    ResultSrc = 2'b00;
                    AdrSrc = 1'b1;
                    MemWrite = 1'b1;

                    ALUSrcA = 2'b00;
                    ALUSrcB = 2'b00;
                    IRWrite = 1'b0;
                    RegWrite = 1'b0;
                    aluOP = 2'b00;
                    Branch = 1'b0;
                    PCUpdate = 1'b0;

                end

                S_ALUWB :
                begin
                    ResultSrc = 2'b00;
                    RegWrite = 1'b1;

                    ALUSrcA = 2'b00;
                    ALUSrcB = 2'b00;
                    AdrSrc = 1'b0;
                    IRWrite = 1'b0;
                    MemWrite = 1'b0;
                    aluOP = 2'b00;
                    Branch = 1'b0;
                    PCUpdate = 1'b0;

                end

                S_MEMWB :
                begin

                    ResultSrc = 2'b01;
                    RegWrite = 1'b1;

                    ALUSrcA = 2'b00;
                    ALUSrcB = 2'b00;
                    AdrSrc = 1'b0;
                    IRWrite = 1'b0;
                    MemWrite = 1'b0;
                    aluOP = 2'b00;
                    Branch = 1'b0;
                    PCUpdate = 1'b0;

                end

                S_LUI:
                begin
                    ALUSrcB = 2'b01;
                    aluOP = 2'b11;

                    ALUSrcA = 2'b00;
                    ResultSrc = 2'b00;
                    AdrSrc = 1'b0;
                    IRWrite = 1'b0;
                    RegWrite = 1'b0;
                    MemWrite = 1'b0;
                    Branch = 1'b0;
                    PCUpdate = 1'b0;


                end


                default:
                begin
                    ALUSrcA = 2'b00;
                    ALUSrcB = 2'b00;
                    ResultSrc = 2'b00;
                    AdrSrc = 1'b0;
                    IRWrite = 1'b0;
                    RegWrite = 1'b0;
                    MemWrite = 1'b0;
                    aluOP = 2'b00;
                    Branch = 1'b0;
                    PCUpdate = 1'b0;
                end

            endcase
        end
    endmodule


    module next_state_logic(input opcodetype op,
                                input  statetype state,
                                output statetype  state_next);


        always_comb
            case(state)
                S_FETCH:
                    state_next = S_DECODE;
                S_DECODE:
                begin
                    if(op == lw_op | op == sw_op)
                        state_next = S_MEMADR;
                    if(op == r_type_op)
                        state_next = S_EXECUTER;
                    if(op == i_type_alu_op)
                        state_next = S_EXECUTEL;
                    if(op == jal_op)
                        state_next = S_JAL;
                    if(op == beq_op)
                        state_next = S_BEQ;
                    if(op == lui_op)
                        state_next = S_LUI;
                end

                S_MEMADR:
                begin
                    if(op == lw_op)
                        state_next = S_MEMREAD;
                    if(op == sw_op)
                        state_next = S_MEMWRITE;
                end
                S_EXECUTER:
                    state_next = S_ALUWB;
                S_EXECUTEL:
                    state_next = S_ALUWB;
                S_JAL:
                    state_next = S_ALUWB;
                S_LUI:
                    state_next = S_ALUWB;
                S_BEQ:
                    state_next = S_FETCH;
                S_MEMREAD:
                    state_next = S_MEMWB;
                S_MEMWRITE:
                    state_next = S_FETCH;
                S_ALUWB:
                    state_next = S_FETCH;
                default:
                    state_next = S_FETCH;
            endcase
        endmodule

        module controller_fsm(  input  logic       clk,
                                    input  logic       reset,
                                    input  opcodetype  op,
                                    output logic [1:0] ALUSrcA, ALUSrcB,
                                    output logic [1:0] ResultSrc,
                                    output logic       AdrSrc,
                                    output logic       IRWrite,
                                    output logic       RegWrite, MemWrite,
                                    output logic [1:0] aluOP,
                                    output logic       Branch,
                                    output logic       PCUpdate);

            statetype state, state_next;

            //state register
            state_register stateRegister(clk, reset, state_next, state);

            //next state logic
            next_state_logic nextStateLogic(op, state, state_next);


            //output logic
            output_logic outputLogic(state, ALUSrcA, ALUSrcB, ResultSrc, AdrSrc, IRWrite, RegWrite, MemWrite, aluOP, Branch, PCUpdate);

        endmodule
