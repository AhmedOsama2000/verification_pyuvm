class transaction;
	
	// holds the I/O of the DUT to pass to other classes
    logic        rst_n;
    logic        en;
    logic [7:0]  A;
    logic [7:0]  B;
    logic [2:0]  OP;
    logic [15:0] result;
    logic [15:0] done;

endclass