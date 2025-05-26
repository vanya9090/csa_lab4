from enum import Enum 
from dataclasses import dataclass
from typing import Callable, Dict, Any, ClassVar
from isa import Opcode, Term, Instruction

class Signal(Enum):
    LATCH_ADDRESS_REGISTER : int = 0
    LATCH_DATA_REGISTER : int = 1
    LATCH_STACK_POINTER_REGISTER : int = 2
    
    LATCH_PROGRAM_COUNTER : int = 3
    LATCH_MPROGRAM_COUNTER : int = 4
    LATCH_INSTRUCTION : int = 11
    TICK : int = 12

    LATCH_LEFT_ALU : int = 5
    LATCH_RIGHT_ALU : int = 6
    EXECUTE_ALU : int = 13

    LATCH_REGISTER : int = 7

    READ : int = 8
    WRITE : int = 9

    LATCH_MEMORY : int = 14
    LATCH_N : int = 15

    ZERO: int = 10


class Sel:
    class DataRegister(Enum):
        MEMORY : int = 0
        ALU: int = 1
    class AddressRegister(Enum):
        CONTROL_UNIT : int = 0
        ALU :int = 1
        STACK_POINTER_REGISTER : int = 2
    class ProgramCounter(Enum):
        JUMP : int = 0
        NEXT : int = 1
    class MProgramCounter(Enum):
        OPCODE : int = 0
        ZERO : int = 1
        N : int = 2
        PLUS_1 : int = 4
    class LeftALU(Enum):
        REGISTER : int = 0
        VALUE : int = 1
        ZERO : int = 2
        PLUS_1 : int = 3
        MINUS_1 : int = 4
    class RightALU(Enum):
        REGISTER : int = 0
        VALUE : int = 1
        DATA_REGISTER : int = 2
        PLUS_1 : int = 3
        MINUS_1 : int = 4
        ZERO : int = 5
    class Register(Enum):
        REGISTER : int = 0
        # VALUE : int = 1
        ALU : int = 2
        DATA_REGISTER : int = 3
    class N(Enum):
        DECODER : int = 0
        MINUS_1 : int = 1
        ZERO : int = 2



class ALU:
    class Flags(Enum):
        ZERO : int = 0
        CARRY : int = 1
        OVERFLOW : int = 2
        NEGATIVE : int = 3
    
    class Operations(Enum):
        ADD : int = 0
        SUB : int = 1
        AND : int = 2
        OR : int = 3
        MUL : int = 4
        DIV : int = 5
        RMD : int = 6

    def __init__(self, datapath : "DataPath"):
        self.datapath = datapath

        self.__left_term : int = 0
        self.__right_term : int = 0
        self.result : int = 0
        self.flags : dict[ALU.Flags, bool] = {
            self.Flags.ZERO : False,
            self.Flags.CARRY: False,
            self.Flags.OVERFLOW: False,
            self.Flags.NEGATIVE: False
        }
        self.__operations : dict[ALU.Operations, Callable[[int, int], int]] = {
            self.Operations.ADD : lambda x, y : x + y,
            self.Operations.SUB : lambda x, y : x - y,
            self.Operations.AND : lambda x, y : x & y,
            self.Operations.OR : lambda x, y : x | y,
            self.Operations.MUL : lambda x, y : x * y,
            self.Operations.DIV : lambda x, y : x / y,
            self.Operations.RMD : lambda x, y : x % y
        }

    def __set_flags(self) -> None:
        self.flags[self.Flags.ZERO] = self.result == 0
        self.flags[self.Flags.NEGATIVE] = self.result < 0

    # left alu only can manipulate left_register
    def latch_left_alu(self, sel : Sel.LeftALU) -> None:
        assert isinstance(sel, Sel.LeftALU), "selector must be LeftALU selector"

        if sel == Sel.LeftALU.REGISTER:
            self.__left_term = self.datapath.registers[self.datapath.left_register]
        if sel == Sel.LeftALU.ZERO:
            self.__left_term = 0
        if sel == Sel.LeftALU.PLUS_1:
            self.__left_term = 1
        if sel == Sel.LeftALU.MINUS_1:
            self.__left_term = -1
    
    # right alu only can manipulate right_register
    def latch_right_alu(self, sel : Sel.RightALU) -> None:
        assert isinstance(sel, Sel.RightALU), "selector must be RightALU selector"

        if sel == Sel.RightALU.REGISTER:
            self.__right_term = self.datapath.registers[self.datapath.right_register]
        if sel == Sel.RightALU.DATA_REGISTER:
            self.__right_term = self.datapath.data_register
        if sel == Sel.RightALU.PLUS_1:
            self.__right_term = 1
        if sel == Sel.RightALU.MINUS_1:
            self.__right_term = -1
        if sel == Sel.RightALU.ZERO:
            self.__right_term = 0

    def perform(self, operation : Operations) -> None:
        self.result = self.__operations[operation](self.__left_term, self.__right_term)
        print(self.__left_term, self.__right_term, self.result)
        self.__set_flags()


class Registers:
    class Registers(Enum):
        RSP : int = 0
        AR : int = 1
        DR : int = 2
        R0 : int = 3
        R1 : int = 4
        R2 : int = 5
        R3 : int = 6
        R4 : int = 7
        R5 : int = 8
        R6 : int = 9
        R7 : int = 10
    
    def __init__(self):
        self.registers_value : dict[Registers.Registers, int] = {
            #TODO think about this three registers
            # Registers.Registers.RSP : 0,
            # Registers.Registers.AR : 0,
            # Registers.Registers.DR : 0,
            Registers.Registers.R0 : 0,
            Registers.Registers.R1 : 0,
            Registers.Registers.R2 : 0,
            Registers.Registers.R3 : 0,
            Registers.Registers.R4 : 0,
            Registers.Registers.R5 : 0,
            Registers.Registers.R6 : 0,
            Registers.Registers.R7 : 0,
        }
    
    def __getitem__(self, key : Registers) -> int:
        return self.registers_value[key]
    
    def __setitem__(self, key : Registers, value : int) -> None:
        self.registers_value[key] = value


class Memory:
    def __init__(self, memory_size):
        self.memory = [0] * memory_size
    
    def __getitem__(self, key) -> int:
        return self.memory[key]
    
    def __setitem__(self, key, value) -> None:
        self.memory[key] = value

class ControlUnit:
    def __init__(self, datapath : "DataPath"):
        self.datapath = datapath

        self.program_counter : int = 0
        self.mprogram_counter : int = 0

        self.mem_address : int = 0
        self.n : int = 0

        self.signals : dict[Signal, Callable] = {
            Signal.LATCH_N : self.latch_n,
            Signal.LATCH_INSTRUCTION : self.latch_instruction,
            Signal.LATCH_PROGRAM_COUNTER : self.latch_program_counter,
            Signal.LATCH_MPROGRAM_COUNTER : self.latch_mprogram_counter,
            Signal.LATCH_ADDRESS_REGISTER : self.datapath.latch_address_register,
            Signal.LATCH_DATA_REGISTER : self.datapath.latch_data_register,
            Signal.LATCH_LEFT_ALU: self.datapath.alu.latch_left_alu,
            Signal.LATCH_RIGHT_ALU: self.datapath.alu.latch_right_alu,
            Signal.EXECUTE_ALU: self.datapath.alu.perform,
            Signal.LATCH_REGISTER : self.datapath.latch_register,
            Signal.LATCH_MEMORY : self.datapath.latch_memory,
        }

        self.mprogram : list[tuple[Signal, Sel]] = [
                # instruction fetch (0)
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
                (Signal.LATCH_INSTRUCTION, None),
                (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.OPCODE),

                # MOV register (4)
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER), # src register
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
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
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
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
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),

                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_REGISTER, Sel.Register.ALU),
                (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
                (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

                # MOV indirect address (40)
                (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),

                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),

                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_REGISTER, Sel.Register.ALU),
                (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
                (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

                # INC register (58)
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER), # src register
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.PLUS_1),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_REGISTER, Sel.Register.ALU), # dst register (same src for this command)
                (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
                (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

                # INC mem cell (64)
                (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # address -> DR
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # address -> AR
                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # mem[address] -> DR

                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.PLUS_1),
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU), # mem[address] + 1 -> DR
                (Signal.LATCH_MEMORY, None), # mem[address] + 1 -> mem[address]
                (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
                (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

                # DEC register (79)
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER), # src register
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.MINUS_1),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_REGISTER, Sel.Register.ALU), # dst register (same src for this command)
                (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
                (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

                # DEC mem cell (85)
                (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # address -> DR
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # address -> AR
                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # mem[address] -> DR

                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.MINUS_1),
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU), # mem[address] - 1 -> DR
                (Signal.LATCH_MEMORY, None), # mem[address] - 1 -> mem[address]
                (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
                (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

                # STORE reg direct (100)
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER), # src register
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD), 
                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.ALU), # src_reg -> DR

                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER), # dst register
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # dst_reg -> AR

                (Signal.LATCH_MEMORY, None), # src_reg -> mem[dst_reg]

                (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
                (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

                # STORE reg indirect (111)
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER), # dst register
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # dst_reg -> AR

                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # mem[dst_reg] -> DR
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # mem[dst_reg] -> AR

                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER), # src register
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD), 
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
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # address -> AR

                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
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
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # address -> AR

                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # mem[address] -> DR
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # mem[address] -> AR

                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.REGISTER),
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
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
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # mem[address] -> DR

                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
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
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # mem[address] -> DR

                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
                (Signal.EXECUTE_ALU, ALU.Operations.SUB),
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
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # mem[address] -> DR

                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
                (Signal.EXECUTE_ALU, ALU.Operations.OR),
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
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU),
                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY), # mem[address] -> DR

                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
                (Signal.EXECUTE_ALU, ALU.Operations.OR),
                (Signal.LATCH_REGISTER, Sel.Register.ALU), # dst_reg & mem[address + i] -> dst_reg

                (Signal.LATCH_N, Sel.N.MINUS_1),
                (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.N),

                (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
                (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
        ]

    def decode(self, instruction: Instruction):
        ALU_mem_operations = (Opcode.ADD_mem, Opcode.SUB_mem,
                              Opcode.MUL_mem, Opcode.DIV_mem,
                              Opcode.RMD_mem, Opcode.AND_mem,
                              Opcode.OR_mem, Opcode.EQ_mem,
                              Opcode.NEQ_mem, Opcode.LT_mem,
                              Opcode.GT_mem)
        MOV_codes = (Opcode.MOV_r2r, Opcode.MOV_rd2r,
                     Opcode.MOV_imm2r, Opcode.MOV_da2r,
                     Opcode.MOV_ia2r)
        INC_DEC_codes = (Opcode.INC_mem, Opcode.INC_r,
                         Opcode.DEC_mem, Opcode.DEC_r)
        STORE_codes = (Opcode.STORE_r2rd, Opcode.STORE_r2ri,
                       Opcode.STORE_r2ia, Opcode.STORE_r2da)
        
        self.opcode : Opcode = instruction.opcode
        self.terms : list[Term] = instruction.terms
        print(self.opcode)
        if self.opcode in MOV_codes:
            if self.opcode in (Opcode.MOV_r2r, Opcode.MOV_rd2r):
                self.datapath.select_right_register(self.terms[0].value)
                self.datapath.select_left_register(self.terms[1].value)
            else: 
                self.datapath.select_right_register(self.terms[0].value)

        elif self.opcode in INC_DEC_codes:
            if self.opcode in (Opcode.INC_r, Opcode.DEC_r):
                self.datapath.select_right_register(self.terms[0].value)
                self.datapath.select_left_register(self.terms[0].value)

        elif self.opcode in STORE_codes:
            if self.opcode in (Opcode.STORE_r2rd, Opcode.STORE_r2ri):
                self.datapath.select_right_register(self.terms[0].value)
                self.datapath.select_left_register(self.terms[1].value)
            else:
                self.datapath.select_right_register(self.terms[0].value)

        elif self.opcode in ALU_mem_operations:
            self.n = self.terms[0].value
            self.datapath.select_right_register(self.terms[1].value)
            self.datapath.select_left_register(self.terms[1].value)

        # elif self.opcode in (Opcode.BEQZ, Opcode.BNEZ, Opcode.BGZ, Opcode.BLZ):
        #     self.datapath.select_left_register(self.terms[0])

        # elif self.opcode in (Opcode.PUSH, Opcode.JMP, Opcode.CALL):
        #     if self.terms[0].value == 0:
        #         self.datapath.select_left_register(self.terms[0].value)

        else:
            raise RuntimeError()
            

    def latch_program_counter(self, sel : Sel.ProgramCounter):
        assert isinstance(sel, Sel.ProgramCounter), "selector must be ProgramCounter selector"

        if sel == Sel.ProgramCounter.JUMP:
            pass
        if sel == Sel.ProgramCounter.NEXT:
            self.program_counter += 1

    def latch_mprogram_counter(self, sel : Sel.MProgramCounter):
        assert isinstance(sel, Sel.MProgramCounter), "selector must be MProgramCounter selector"

        if sel == Sel.MProgramCounter.ZERO:
            self.mprogram_counter = 0
        if sel == Sel.MProgramCounter.PLUS_1:
            self.mprogram_counter += 1
        if sel == Sel.MProgramCounter.OPCODE:
            self.mprogram_counter = self.opcode.value
        if sel == Sel.MProgramCounter.N:
            if self.n == 0:
                self.mprogram_counter += 1
            else:
                self.mprogram_counter = self.opcode.value

    def latch_instruction(self):
        self.decode(self.datapath.data_register)

    def latch_n(self, sel : Sel.N):
        assert isinstance(sel, Sel.N), "selector must be N selector"

        if sel == Sel.N.DECODER:
            self.n = self.terms[0]
        if sel == Sel.N.MINUS_1:
            self.n -= 1
        if sel == Sel.N.ZERO:
            self.n = 0

    def execute_signal(self, signal : Signal, *arg):
        self.signals[signal](*arg)

    def run_single_micro(self):
        mpc_now = self.mprogram_counter
        signal, *maybe_sel = self.mprogram[mpc_now]
        print(mpc_now, signal, maybe_sel[0])
        if maybe_sel and maybe_sel[0] is not None:
            self.execute_signal(signal, maybe_sel[0])
        else:
            self.execute_signal(signal)

        if self.mprogram_counter == mpc_now:
            self.mprogram_counter += 1


class DataPath:
    def __init__(self, input_address, output_address):
        self.alu : ALU = ALU(self)
        self.control_unit : ControlUnit = ControlUnit(self)
        self.registers : Registers = Registers()
        self.memory = Memory(1024)

        self.data_register : int = 0
        self.address_register : int = 0
        # TODO make list of chosen registers logic
        self.chosen_registers : list[Registers.Registers] = None
        self.left_register : Registers.Registers = None
        self.right_register : Registers.Registers = None

        self.input_address : int = input_address
        self.output_address : int = output_address

    def select_left_register(self, register : Registers.Registers):
        self.left_register = register

    def select_right_register(self, register : Registers.Registers):
        self.right_register = register

    def latch_data_register(self, sel : Sel.DataRegister):
        assert isinstance(sel, Sel.DataRegister), "selector must be DataRegister selector"

        if sel == Sel.DataRegister.ALU:
            self.data_register = self.alu.result
        elif sel == Sel.DataRegister.MEMORY:
            self.data_register = self.memory[self.address_register]
            print('latch DR:', self.data_register, self.address_register)
        
    def latch_address_register(self, sel : Sel.AddressRegister):
        assert isinstance(sel, Sel.AddressRegister), "selector must be AddressRegister selector"

        if sel == Sel.AddressRegister.CONTROL_UNIT:
            self.address_register = self.control_unit.program_counter
        if sel == Sel.AddressRegister.ALU:
            self.address_register = self.alu.result
        # elif sel == Sel.AddressRegister.REGISTER:
        #     self.address_register = self.registers[self.left_register]
        # elif sel == Sel.AddressRegister.STACK_POINTER_REGISTER: # TODO remove RSP 
        #     self.address_register = self.registers[Registers.Registers.RSP]

    def latch_register(self, sel : Sel.Register):
        assert isinstance(sel, Sel.Register), "selector must be Register selector"

        if sel == Sel.Register.ALU:
            self.registers[self.right_register] = self.alu.result
        elif sel == Sel.Register.DATA_REGISTER:
            self.registers[self.right_register] = self.data_register
        elif sel == Sel.Register.REGISTER:
            self.registers[self.right_register] == self.registers[self.left_register]

    def latch_memory(self):
        print(self.address_register, self.data_register)
        self.memory[self.address_register] = self.data_register