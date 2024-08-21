class sequencer;

	typedef enum {ADD, MUL, AND, OR, XOR, NOTA} en_opcodes;

	en_opcodes opcodes;
	
	// create a single transaction ato send it to the driver
	transaction tn;

	function new();
		tn = new(); 
	endfunction 

	task init();
		tn.rst_n = 0;
		tn.A = 8'b0;
		tn.B = 8'b0;
		tn.OP = opcodes.first();
	endtask

	task send_stim;
		tn.en = 1;
		tn.rst_n = 1;
		tn.A  = $random;
		tn.B  = $random;
		opcodes = opcodes.next();
		tn.OP = opcodes;
	endtask

endclass