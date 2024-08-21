class env;
	driver drv;
	monitor mon;
	sequencer seq;

	function new();
		drv = new;
		mon = new;
		seq = new;
	endfunction

	task init_test(virtual alu_intf al_intf);
	    seq.init(); 
	    drv.tn = seq.tn;  // pass the transction created by the sequencer to the driver  
	    drv.pass_data(al_intf);
	    mon.get_data(al_intf);
	endtask

	task execute_test (virtual alu_intf al_intf);
		seq.send_stim();
		drv.tn = seq.tn;
		drv.pass_data(al_intf);
		mon.get_data(al_intf);
	endtask

endclass