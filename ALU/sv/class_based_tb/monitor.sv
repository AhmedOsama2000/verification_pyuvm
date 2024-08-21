class monitor;
	// pass the data (output) from the virtual interface (from DUT) to transction
	transaction tn;
	function new();
		tn = new();
	endfunction : new
	task get_data(virtual alu_intf al_intf);

		tn.result = al_intf.result;
		tn.done = al_intf.done;

	endtask

endclass