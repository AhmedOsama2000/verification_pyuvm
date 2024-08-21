`include "interface.sv"
module testbench;

    import alu_pkg::*;
    alu_intf intf1(); 
    virtual alu_intf vif; // create virtual interface to communicate with class hirarchy
    env alu_env;

    always begin
        #10 intf1.CLK = ~intf1.CLK; 
    end

    alu dut(
        .CLK(intf1.CLK),
        .rst_n(intf1.rst_n),
        .en(intf1.en),
        .A(intf1.A),
        .B(intf1.B),
        .OP(intf1.OP),
        .result(intf1.result),
        .done(intf1.done)
    ); 

    initial begin
        vif = intf1;
        alu_env = new();
        alu_env.init_test(vif); // vif is actual argument 
        @(posedge intf1.CLK);
        for (int i = 0; i < 10; i++) begin
            alu_env.execute_test(vif);
            @(posedge intf1.CLK);
        end
        @(posedge intf1.CLK);
        $stop;
    end

endmodule 