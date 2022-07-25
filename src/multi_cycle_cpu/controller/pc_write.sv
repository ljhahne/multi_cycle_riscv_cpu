`timescale 1ns/1ps

module pc_write(    input logic Zero,
                        input logic Branch,
                        input logic PCUpdate,
                        output logic PCWrite
                   );
    assign PCWrite = (Zero & Branch) | PCUpdate;
endmodule
