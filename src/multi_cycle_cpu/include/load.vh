`ifndef LOAD
`define LOAD

typedef enum logic[2:0] {   
                            lb=3'b000, 
                            lh=3'b001, 
                            lw=3'b010,
                            lbu=3'b011, 
                            lhu=3'b100

                        } Loadtype;

typedef enum logic[2:0] {   
    
                            flb=3'b000, 
                            flh=3'b001, 
                            flw=3'b010,
                            flbu=3'b100, 
                            flhu=3'b101
                            
} LoadFunct3;


`endif