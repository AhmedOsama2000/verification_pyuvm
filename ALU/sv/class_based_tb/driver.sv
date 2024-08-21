class driver;
	// pass the data from transaction to DUT throught virtual interface
	transaction tn;
	task pass_data(virtual alu_intf al_intf);

		al_intf.rst_n = tn.rst_n;
		al_intf.en = tn.en;
		al_intf.A = tn.A;
		al_intf.B = tn.B;
		al_intf.OP = tn.OP;

	endtask

endclass