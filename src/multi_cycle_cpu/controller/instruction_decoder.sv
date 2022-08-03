`timescale 1ns/1ps
`include "riscv.vh"

module instruction_decoder(input  opcodetype  op,
                               output logic [2:0] ImmSrc);

    // only ImmSrc of single cycle instruction decoder
    always_comb
        case(op)
            lw_op           :
                ImmSrc = 3'b000;
            sw_op           :
                ImmSrc = 3'b001;
            r_type_op       :
                ImmSrc = 3'bxxx;
            beq_op          :
                ImmSrc = 3'b010;
            i_type_alu_op   :
                ImmSrc = 3'b000;
            jal_op          :
                ImmSrc = 3'b011;
            lui_op            :
                ImmSrc = 3'b100;

            default        :
                ImmSrc = 3'bxxx;
        endcase

    endmodule
