`timescale 1ns/1ps

`include "load.vh"


module load_extend(
    input Loadtype loadtype,
    input logic [31:0] ReadData,
    output logic [31:0] Data
);


    always_comb
        case(loadtype)
            lb:
                Data = {{24{ReadData[7]}}, ReadData[7:0]};
            lh:
                Data = {{16{ReadData[15]}}, ReadData[15:0]};
            lw: 
                Data = ReadData;
            lbu:
                Data = {{24{1'b0}}, ReadData[7:0]};
            lhu:
                Data = {{16{1'b0}}, ReadData[15:0]};
            default:
                Data = 32'bx;
        endcase


endmodule