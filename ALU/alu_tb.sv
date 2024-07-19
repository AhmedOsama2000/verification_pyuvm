module alu_tb;

    logic        rst_n_tb;
    bit          CLK_tb;
    logic        en_tb;
    logic [7:0]  A_tb;
    logic [7:0]  B_tb;
    logic [2:0]  OP_tb;
    logic [15:0] result_tb;

    logic [15:0] expected_result;

    int correct_cases;
    int incorrect_cases;

    localparam ADD     = 3'b000;
    localparam MUL     = 3'b001;
    localparam AND     = 3'b010;
    localparam OR      = 3'b011;
    localparam XOR     = 3'b100;
    localparam NOTA    = 3'b101;

    always begin
    	#1
    	CLK_tb  = ~CLK_tb;
    end


    initial begin
    	// initialize the dut
    	rst_n_tb = 1'b0;
    	en_tb = 1'b0;

    	repeat (5) @(negedge CLK_tb);
        en_tb = 1'b1;
        rst_n_tb = 1'b1;
        for (int i; i < 50; i++) begin
            A_tb  = $random;
            B_tb  = $random;
            OP_tb = $urandom % 6;
            @(negedge CLK_tb);
            chk_res();
        end

        @(negedge CLK_tb);
        en_tb = 1'b1;

        repeat (5) @(negedge CLK_tb);

        $display("correct_cases: %d",correct_cases);
        $display("incorrect_cases: %d",incorrect_cases);
        $stop;


    end

task chk_res;
    case (OP_tb)
        ADD: expected_result  = A_tb + B_tb;
        MUL: expected_result  = A_tb * B_tb;
        AND: expected_result  = A_tb & B_tb;
        OR: expected_result   = A_tb | B_tb;
        XOR: expected_result  = A_tb ^ B_tb;
        NOTA: expected_result = {{8{1'b0}},~A_tb};
    endcase

    $display("A: %0d, B: %0d, OP: %0d, dut_result: %0d, actual_result: %0d", A_tb, B_tb, OP_tb, result_tb, expected_result);
    if (result_tb == expected_result)
        correct_cases++;
    else
        incorrect_cases++;
endtask

alu dut (
    .rst_n(rst_n_tb),
    .CLK(CLK_tb),
    .en(en_tb),
    .A(A_tb),
    .B(B_tb),
    .OP(OP_tb),
    .result(result_tb)
);

endmodule