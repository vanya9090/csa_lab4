from enums import ALUOperations, Sel, Signal

mprogram = [
    # instruction fetch (0)
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_INSTRUCTION, None),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.OPCODE),
    # MOV register (4)
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),  # src register
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),  # dst register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # MOV register direct (10)
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),  # src register
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # MOV immediate (20)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),  # for get imm value
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_REGISTER, Sel.Register.DR),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # MOV direct address (26)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),

    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
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
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),

    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),

    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # INC register (58)
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),  # src register
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.PLUS_1),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # dst register (same src for this command)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # INC mem cell (64)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # address -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),  # address -> AR
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.PLUS_1),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),  # mem[address] + 1 -> DR
    (Signal.LATCH_MEMORY, None),  # mem[address] + 1 -> mem[address]
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # DEC register (79)
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),  # src register
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.MINUS_1),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # dst register (same src for this command)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # DEC mem cell (85)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # address -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),  # address -> AR
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.MINUS_1),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),  # mem[address] - 1 -> DR
    (Signal.LATCH_MEMORY, None),  # mem[address] - 1 -> mem[address]
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # STORE reg direct (100)
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),  # src register
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),  # src_reg -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),  # dst register
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),  # dst_reg -> AR
    (Signal.LATCH_MEMORY, None),  # src_reg -> mem[dst_reg]
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # STORE reg indirect (111)
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),  # dst register
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),  # dst_reg -> AR
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[dst_reg] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),  # mem[dst_reg] -> AR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),  # src register
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),  # src_reg + 0 -> DR
    (Signal.LATCH_MEMORY, None),  # src_reg -> mem[mem[dst_reg]]
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # STORE mem direct (127)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # address -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),  # address -> AR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),  # src_reg -> DR
    (Signal.LATCH_MEMORY, None),  # src_reg -> mem[address]
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # STORE mem indirect (141)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # address -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),  # address -> AR
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),  # mem[address] -> AR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),  # src_reg -> DR
    (Signal.LATCH_MEMORY, None),  # src_reg -> mem[mem[address]]
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # NADD direct address (160)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),  # dst_reg + mem[address + i] -> dst_reg
    (Signal.LATCH_N, Sel.N.MINUS_1),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.N),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # NSUB direct address (176)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.SUB),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),  # dst_reg - mem[address + i] -> dst_reg
    (Signal.LATCH_N, Sel.N.MINUS_1),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.N),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # NOR direct address (192)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.OR),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),  # dst_reg | mem[address + i] -> dst_reg
    (Signal.LATCH_N, Sel.N.MINUS_1),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.N),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # AND direct address (208)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.OR),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),  # dst_reg & mem[address + i] -> dst_reg
    (Signal.LATCH_N, Sel.N.MINUS_1),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.N),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # JUMP register (224)
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_FLAG, Sel.Flag.NONE),
    (Signal.LATCH_JUMP, Sel.Jump.ALU),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.CONDITION),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # JUMP immediate (231)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_JUMP, Sel.Jump.ALU),
    (Signal.LATCH_FLAG, Sel.Flag.NONE),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.CONDITION),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # BEQZ (241)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),  # mem[address] -> ALU
    (Signal.LATCH_JUMP, Sel.Jump.ALU),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),  # set_flags(src_reg)
    (Signal.LATCH_FLAG, Sel.Flag.ZERO),
    (Signal.LATCH_INVERSE, Sel.Inverse.IDENTITY),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.CONDITION),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # BNEZ (255)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_JUMP, Sel.Jump.ALU),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),  # set_flags(src_reg)
    (Signal.LATCH_FLAG, Sel.Flag.ZERO),
    (Signal.LATCH_INVERSE, Sel.Inverse.INVERSE),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.CONDITION),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # BGZ (269)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_JUMP, Sel.Jump.ALU),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),  # set_flags(src_reg)
    (Signal.LATCH_FLAG, Sel.Flag.NEGATIVE),
    (Signal.LATCH_INVERSE, Sel.Inverse.INVERSE),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.CONDITION),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # BLZ (283)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_JUMP, Sel.Jump.ALU),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_FLAG, Sel.Flag.NEGATIVE),
    (Signal.LATCH_INVERSE, Sel.Inverse.IDENTITY),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.CONDITION),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # CALL immediate (297)
    # store ret address
    (Signal.LATCH_RSP, Sel.RSP.MINUS_1),  # RSP --
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.RSP),  # rsp -> AR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.PC),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.PLUS_2),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),
    (Signal.LATCH_MEMORY, None),  # PC + 1 -> mem[RSP]
    # jump
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_JUMP, Sel.Jump.ALU),
    (Signal.LATCH_FLAG, Sel.Flag.NONE),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.CONDITION),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # RET (314)
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.RSP),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_JUMP, Sel.Jump.ALU),
    (Signal.LATCH_FLAG, Sel.Flag.NONE),
    (Signal.LATCH_RSP, Sel.RSP.PLUS_1),  # RSP ++
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.CONDITION),  # mem[RSP+1] -> PC
    # (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),  # PC + 1 -> PC
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # NMUL direct address (321)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.MUL),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),  # dst_reg + mem[address + i] -> dst_reg
    (Signal.LATCH_N, Sel.N.MINUS_1),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.N),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # ADD reg to reg (337)
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # ADD mem to reg (343)(6)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+2] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+2] -> right_alu
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # mem[address+1] + mem[address+2] -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # ADD mem to mem (359)(16)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+2] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+2] -> right_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),
    (Signal.LATCH_MEMORY, None),  # mem[address+1] + mem[address+2] -> mem[address+3]
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # ADD mix1 to reg (380)(21)
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),  # src_reg -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+1] -> right_alu
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # src_reg + mem[address+2] -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # MOV mem to mem (391)(11)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+1] -> right_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),
    (Signal.LATCH_MEMORY, None),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # SUB reg to reg (407)
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.SUB),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # SUB mem to reg (413)(6)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+2] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+2] -> right_alu
    (Signal.EXECUTE_ALU, ALUOperations.SUB),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # mem[address+1] - mem[address+2] -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # SUB mem to mem (429)(16)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+2] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+2] -> right_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.EXECUTE_ALU, ALUOperations.SUB),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),
    (Signal.LATCH_MEMORY, None),  # mem[address+1] - mem[address+2] -> mem[address+3]
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # SUB mix1 to reg (450)(21)
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),  # src_reg -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+1] -> right_alu
    (Signal.EXECUTE_ALU, ALUOperations.SUB),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # src_reg - mem[address+2] -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # SUB mix2 to reg (461)(11)
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),  # src_reg -> right_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.EXECUTE_ALU, ALUOperations.SUB),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # mem[address+2] - src_reg -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # MUL reg to reg (472)
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.MUL),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # MUL mem to reg (413)(6)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+2] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+2] -> right_alu
    (Signal.EXECUTE_ALU, ALUOperations.MUL),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # mem[address+1] - mem[address+2] -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # MUL mem to mem (429)(16)
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+2] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+2] -> right_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.EXECUTE_ALU, ALUOperations.MUL),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),
    (Signal.LATCH_MEMORY, None),  # mem[address+1] - mem[address+2] -> mem[address+3]
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # MUL mix1 to reg (450)(21
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),  # src_reg -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+1] -> right_alu
    (Signal.EXECUTE_ALU, ALUOperations.MUL),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # src_reg - mem[address+2] -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # DIV reg to reg
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.DIV),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # DIV mem to reg
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+2] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+2] -> right_alu
    (Signal.EXECUTE_ALU, ALUOperations.DIV),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # mem[address+1] - mem[address+2] -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # DIV mem to mem
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+2] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+2] -> right_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.EXECUTE_ALU, ALUOperations.DIV),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),
    (Signal.LATCH_MEMORY, None),  # mem[address+1] - mem[address+2] -> mem[address+3]
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # DIV mix1 to reg
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),  # src_reg -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+1] -> right_alu
    (Signal.EXECUTE_ALU, ALUOperations.DIV),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # src_reg - mem[address+2] -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # DIV mix2 to reg
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),  # src_reg -> right_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.EXECUTE_ALU, ALUOperations.DIV),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # mem[address+2] - src_reg -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # RMD reg to reg
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.RMD),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # RMD mem to reg
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+2] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+2] -> right_alu
    (Signal.EXECUTE_ALU, ALUOperations.RMD),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # mem[address+1] - mem[address+2] -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # RMD mem to mem
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+2] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+2] -> right_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.EXECUTE_ALU, ALUOperations.RMD),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),
    (Signal.LATCH_MEMORY, None),  # mem[address+1] - mem[address+2] -> mem[address+3]
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # RMD mix1 to reg
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),  # src_reg -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+1] -> right_alu
    (Signal.EXECUTE_ALU, ALUOperations.RMD),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # src_reg - mem[address+2] -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # RMD mix2 to reg
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),  # src_reg -> right_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.EXECUTE_ALU, ALUOperations.RMD),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # mem[address+2] - src_reg -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # AND reg to reg
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.AND),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # AND mem to reg
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+2] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+2] -> right_alu
    (Signal.EXECUTE_ALU, ALUOperations.AND),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # mem[address+1] - mem[address+2] -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # AND mem to mem
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+2] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+2] -> right_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.EXECUTE_ALU, ALUOperations.AND),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),
    (Signal.LATCH_MEMORY, None),  # mem[address+1] - mem[address+2] -> mem[address+3]
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # AND mix1 to reg
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),  # src_reg -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+1] -> right_alu
    (Signal.EXECUTE_ALU, ALUOperations.AND),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # src_reg - mem[address+2] -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # OR reg to reg
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.OR),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # OR mem to reg
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+2] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+2] -> right_alu
    (Signal.EXECUTE_ALU, ALUOperations.OR),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # mem[address+1] - mem[address+2] -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # OR mem to mem
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+2] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+2] -> right_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.EXECUTE_ALU, ALUOperations.OR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),
    (Signal.LATCH_MEMORY, None),  # mem[address+1] - mem[address+2] -> mem[address+3]
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # OR mix1 to reg
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),  # src_reg -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+1] -> right_alu
    (Signal.EXECUTE_ALU, ALUOperations.OR),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # src_reg - mem[address+2] -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # XOR reg to reg
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),
    (Signal.EXECUTE_ALU, ALUOperations.XOR),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # XOR mem to reg
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+2] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+2] -> right_alu
    (Signal.EXECUTE_ALU, ALUOperations.XOR),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # mem[address+1] - mem[address+2] -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # XOR mem to mem
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.DR),  # mem[address+1] -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+2] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+2] -> right_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.EXECUTE_ALU, ALUOperations.XOR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),
    (Signal.LATCH_MEMORY, None),  # mem[address+1] - mem[address+2] -> mem[address+3]
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # XOR mix1 to reg
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),  # src_reg -> left_alu
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.DR),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),  # mem[address+1] -> DR
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),  # mem[address+1] -> right_alu
    (Signal.EXECUTE_ALU, ALUOperations.XOR),
    (
        Signal.LATCH_REGISTER,
        Sel.Register.ALU,
    ),  # src_reg - mem[address+2] -> dst_register
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # PUSH register +11
    (Signal.LATCH_RSP, Sel.RSP.MINUS_1),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.RSP),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU),
    (Signal.LATCH_MEMORY, None),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # POP register + 9
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.RSP),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
    (Signal.LATCH_REGISTER, Sel.Register.DR),
    (Signal.LATCH_RSP, Sel.RSP.PLUS_1),
    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
    # HLT + 6
    (Signal.HLT, None),
    # MOV register indirect + 1
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),  # src register
    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),

    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
    (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),

    (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DR),
    (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
    (Signal.EXECUTE_ALU, ALUOperations.ADD),
    (Signal.LATCH_REGISTER, Sel.Register.ALU),

    (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
    (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
]
