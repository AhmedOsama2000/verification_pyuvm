// unsigned alu
module alu (
    // input
    input wire       rst_n,
    input wire       CLK,
    input wire       en,
    input wire [7:0] A,
    inout wire [7:0] B,
    input wire [2:0] OP,
    // output
    output reg [15:0] result
);

localparam ADD     = 3'b000;
localparam MUL     = 3'b001;
localparam AND     = 3'b010;
localparam OR      = 3'b011;
localparam XOR     = 3'b100;
localparam NOTA    = 3'b101;


always @(posedge CLK) begin
    if (!rst_n) begin
        result <= 16'b0;
    end
    else if (en) begin
        if (OP == ADD) begin
            result <= A + B;
        end
        else if (OP == MUL) begin
            result <= A * B;
        end
        else if (OP == AND) begin
            result <= A & B;
        end
        else if (OP == OR) begin
            result <= A | B;
        end
        else if (OP == XOR) begin
            result <= A ^ B;
        end
        else if (OP == NOTA) begin
            result <= {{8{1'b0}},~A};
        end
    end
end

initial begin
	$dumpfile("alu.vcd");
	$dumpvars(1,alu);
end

endmodule