`timescale 1ns/1ps
`include "riscv.vh"

module instruction_decoder(input  opcodetype  op,
                               output logic [1:0] ImmSrc);

    // only ImmSrc of single cycle instruction decoder
    always_comb
        case(op)
            lw_op           :
                ImmSrc = 2'b00;
            sw_op           :
                ImmSrc = 2'b01;
            r_type_op       :
                ImmSrc = 2'bxx;
            beq_op          :
                ImmSrc = 2'b10;
            i_type_alu_op   :
                ImmSrc = 2'b00;
            jal_op          :
                ImmSrc = 2'b11;
            default        :
                ImmSrc = 2'bxx;
        endcase

    endmodule
