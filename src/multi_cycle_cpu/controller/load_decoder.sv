`timescale 1ns/1ps

`include "load.vh"

module load_decoder(
    input  logic [2:0] funct3,
    output logic [2:0] loadtype
    );

    always_comb
        case(funct3)
            flb:
                loadtype = lb;
            
            flh:
                loadtype = lh;
            
            flw:
                loadtype = lw;
            
            flbu:
                loadtype = lbu;
            
            flhu:
                loadtype = lhu;

            default:

                loadtype = 3'bx;
        endcase

endmodule