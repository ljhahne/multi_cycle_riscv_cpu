`timescale 1ns/1ps
`include "riscv.vh"
`include "immsrc.vh"

module instruction_decoder(input  opcodetype  op,
                               output logic [2:0] ImmSrc);

    // only ImmSrc of single cycle instruction decoder
    always_comb
        case(op)
            lw_op           :
                ImmSrc = `IMMSRC_I;
            sw_op           :
                ImmSrc = `IMMSRC_S;
            r_type_op       :
                ImmSrc = 3'bxxx;
            beq_op          :
                ImmSrc = `IMMSRC_B;
            i_type_alu_op   :
                ImmSrc = `IMMSRC_I;
            jal_op          :
                ImmSrc = `IMMSRC_J;
            lui_op            :
                ImmSrc = `IMMSRC_U;

            default        :
                ImmSrc = 3'bxxx;
        endcase

    endmodule
