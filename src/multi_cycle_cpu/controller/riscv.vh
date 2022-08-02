`ifndef RISCV
`define RISCV

typedef enum logic[6:0] {r_type_op=7'b0110011, i_type_alu_op=7'b0010011, lw_op=7'b0000011, sw_op=7'b0100011, beq_op=7'b1100011, jal_op=7'b1101111, lui_op=7'b0110111} opcodetype;
typedef enum logic [10:0] {S_FETCH, S_DECODE, S_MEMADR, S_MEMREAD, S_MEMWB, S_MEMWRITE, S_EXECUTER, S_EXECUTEL, S_ALUWB, S_BEQ, S_JAL} statetype;


`endif