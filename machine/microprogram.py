from machine.enums import Signal, Sel, ALUOperations

mprogram = [
# instruction fetch (0)
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
(Signal.LATCH_INSTRUCTION, None),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.OPCODE),

# MOV register (4)
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER), # src register
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_REGISTER, Sel.Register.ALU), # dst register
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

# MOV register indirect (10)
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER), # src register
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_REGISTER, Sel.Register.ALU),
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

# MOV immediate (20)
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT), # for get imm value
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
(Signal.LATCH_REGISTER, Sel.Register.DATA_REGISTER),
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

# MOV direct address (26)
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),

(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_REGISTER, Sel.Register.ALU),
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

# MOV indirect address (40)
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),

(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.EXECUTE_ALU, ALUOperations.ADD),

(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_REGISTER, Sel.Register.ALU),
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

# INC register (58)
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER), # src register
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.PLUS_1),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_REGISTER, Sel.Register.ALU), # dst register (same src for this command)
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

# INC mem cell (64)
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # address -> DR
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # address -> AR
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # mem[address] -> DR

(Signal.LATCH_LEFT_ALU, Sel.LeftALU.PLUS_1),
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU), # mem[address] + 1 -> DR
(Signal.LATCH_MEMORY, None), # mem[address] + 1 -> mem[address]
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

# DEC register (79)
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER), # src register
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.MINUS_1),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_REGISTER, Sel.Register.ALU), # dst register (same src for this command)
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

# DEC mem cell (85)
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # address -> DR
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # address -> AR
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # mem[address] -> DR

(Signal.LATCH_LEFT_ALU, Sel.LeftALU.MINUS_1),
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU), # mem[address] - 1 -> DR
(Signal.LATCH_MEMORY, None), # mem[address] - 1 -> mem[address]
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

# STORE reg direct (100)
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER), # src register
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD), 
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU), # src_reg -> DR

(Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER), # dst register
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # dst_reg -> AR

(Signal.LATCH_MEMORY, None), # src_reg -> mem[dst_reg]

(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

# STORE reg indirect (111)
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER), # dst register
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # dst_reg -> AR

(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # mem[dst_reg] -> DR
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # mem[dst_reg] -> AR

(Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER), # src register
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD), 
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU), # src_reg + 0 -> DR

(Signal.LATCH_MEMORY, None), # src_reg -> mem[mem[dst_reg]]

(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

# STORE mem direct (127)
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # address -> DR
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # address -> AR

(Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU), # src_reg -> DR

(Signal.LATCH_MEMORY, None), # src_reg -> mem[address]  

(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

# STORE mem indirect (141)
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # address -> DR
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # address -> AR

(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # mem[address] -> DR
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # mem[address] -> AR

(Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU), # src_reg -> DR

(Signal.LATCH_MEMORY, None), # src_reg -> mem[mem[address]]

(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

# ADD direct address (160)
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # mem[address] -> DR
        
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_REGISTER, Sel.Register.ALU), # dst_reg + mem[address + i] -> dst_reg

(Signal.LATCH_N, Sel.N.MINUS_1),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.N),

(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

# SUB direct address (176)
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # mem[address] -> DR

(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
(Signal.EXECUTE_ALU, ALUOperations.SUB),
(Signal.LATCH_REGISTER, Sel.Register.ALU), # dst_reg - mem[address + i] -> dst_reg

(Signal.LATCH_N, Sel.N.MINUS_1),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.N),

(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

# OR direct address (192)
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # mem[address] -> DR

(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
(Signal.EXECUTE_ALU, ALUOperations.OR),
(Signal.LATCH_REGISTER, Sel.Register.ALU), # dst_reg | mem[address + i] -> dst_reg
                
(Signal.LATCH_N, Sel.N.MINUS_1),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.N),

(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

# AND direct address (208)
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
(Signal.EXECUTE_ALU, ALUOperations.ADD),
(Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
(Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # mem[address] -> DR

(Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
(Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
(Signal.EXECUTE_ALU, ALUOperations.OR),
(Signal.LATCH_REGISTER, Sel.Register.ALU), # dst_reg & mem[address + i] -> dst_reg

(Signal.LATCH_N, Sel.N.MINUS_1),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.N),
                
(Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
(Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
]