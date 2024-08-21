interface alu_intf;

    logic        rst_n;
    bit          CLK;
    logic        en;
    logic [7:0]  A;
    logic [7:0]  B;
    logic [2:0]  OP;
    logic [15:0] result;
    logic [15:0] done;
    
endinterface : alu_intf