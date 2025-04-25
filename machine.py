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
    LATCH_VALUE_REGISTER : int = 14
    TICK : int = 12

    LATCH_LEFT_ALU : int = 5
    LATCH_RIGHT_ALU : int = 6
    EXECUTE_ALU : int = 13

    LATCH_REGISTER : int = 7

    READ : int = 8
    WRITE : int = 9

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
        TYPE : int = 2
    class LeftALU(Enum):
        REGISTER : int = 0
        VALUE : int = 1
        ZERO : int = 2
    class RightALU(Enum):
        REGISTER : int = 0
        VALUE : int = 1
        DATA_REGISTER : int = 2
        PLUS_1 : int = 3
        MINUS_1 : int = 4
        ZERO : int = 5
    class Register(Enum):
        REGISTER : int = 0
        VALUE : int = 1
        ALU : int = 2
        DATA_REGISTER : int = 3


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
            self.Operations.AND : lambda x, y : x and y,
            self.Operations.OR : lambda x, y : x or y,
            self.Operations.MUL : lambda x, y : x * y,
            self.Operations.DIV : lambda x, y : x / y,
            self.Operations.RMD : lambda x, y : x % y
        }

    def __set_flags(self) -> None:
        self.flags[self.Flags.ZERO] = self.result == 0
        self.flags[self.Flags.NEGATIVE] = self.result < 0

    def latch_left_alu(self, sel : Sel.LeftALU) -> None:
        assert isinstance(sel, Sel.LeftALU), "selector must be LeftALU selector"

        if sel == Sel.LeftALU.REGISTER:
            self.__left_term = self.datapath.registers[self.datapath.src_register]
        if sel == Sel.LeftALU.VALUE:
            self.__left_term = self.datapath.control_unit.value_register
        if sel == Sel.LeftALU.ZERO:
            self.__left_term = 0
    
    def latch_right_alu(self, sel : Sel.RightALU) -> None:
        assert isinstance(sel, Sel.RightALU), "selector must be RightALU selector"

        if sel == Sel.RightALU.REGISTER:
            self.__right_term = self.datapath.registers[self.datapath.src_register]
        if sel == Sel.RightALU.VALUE:
            self.__right_term = self.datapath.control_unit.value_register
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
    
    # def latch_register(self, sel : Sel.Register, register : Registers):
    #     assert isinstance(sel, Sel.Register), "selector must be Register selector"

    #     if sel == Sel.Register.ALU:
    #         self.registers_value[register] = 


class Memory:
    def __init__(self, memory_size):
        self.memory = [0] * memory_size
    
    def __getitem__(self, key) -> int: # TODO rewrite to address register
        return self.memory[key]
    
    def __setitem__(self, key, value) -> None:
        self.memory[key] = value


class ControlUnit:
    def __init__(self, datapath : "DataPath"):
        self.datapath = datapath

        self.program_counter : int = 0
        self.mprogram_counter : int = 0

        self.value_register : int = 0
        self.mem_address : int = 0
        self.n : int = 0

        self.signals : dict[Signal, Callable] = {
            Signal.LATCH_VALUE_REGISTER : self.latch_value_register,
            Signal.LATCH_INSTRUCTION : self.latch_instruction,
            Signal.LATCH_PROGRAM_COUNTER : self.latch_program_counter,
            Signal.LATCH_MPROGRAM_COUNTER : self.latch_mprogram_counter,
            Signal.LATCH_ADDRESS_REGISTER : self.datapath.latch_address_register,
            Signal.LATCH_DATA_REGISTER : self.datapath.latch_data_register,
            Signal.LATCH_LEFT_ALU: self.datapath.alu.latch_left_alu,
            Signal.LATCH_RIGHT_ALU: self.datapath.alu.latch_right_alu,
            Signal.EXECUTE_ALU: self.datapath.alu.perform,
            Signal.LATCH_REGISTER : self.datapath.latch_register,
            # Signal.LATCH_STACK_POINTER_REGISTER : self.datapath.la
        }

        self.opcode_to_mPC : dict[Opcode, int] = {
            Opcode.MOV : 1,
        }

        self.mprogram = [
            (
                # instruction fetch
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
                (Signal.LATCH_INSTRUCTION),
                (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.OPCODE),
            ),
            (
                (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.TYPE), # jmp to type
                # MOV register
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER), # src register
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_REGISTER, Sel.Register.ALU), # dst register
                (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
                (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
            ),
            (
                # MOV register indirect
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.REGISTER),
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.ZERO),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.ALU), # src register
                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
                (Signal.LATCH_RIGHT_ALU, Sel.RightALU.DATA_REGISTER),
                (Signal.LATCH_LEFT_ALU, Sel.LeftALU.ZERO),
                (Signal.EXECUTE_ALU, ALU.Operations.ADD),
                (Signal.LATCH_REGISTER, Sel.Register.ALU),
                (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
                (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),
            ),
            (
                # MOV immediate
                (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
                (Signal.LATCH_ADDRESS_REGISTER, Sel.AddressRegister.CONTROL_UNIT),
                (Signal.LATCH_DATA_REGISTER, Sel.DataRegister.MEMORY),
                (Signal.LATCH_REGISTER, Sel.Register.DATA_REGISTER),
                (Signal.LATCH_PROGRAM_COUNTER, Sel.ProgramCounter.NEXT),
                (Signal.LATCH_MPROGRAM_COUNTER, Sel.MProgramCounter.ZERO),

            ),
            (
                # MOV direct address
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
            ),
            (
                # MOV indirect address
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
            ),
        ]

    def decode(self, instruction: Instruction):
        self.opcode : Opcode = instruction.opcode
        self.terms : list[Term] = instruction.terms

        if self.opcode == Opcode.MOV:
            if self.terms[0].value == 0 or self.terms[0].value == 1:
                self.datapath.select_dst_register(self.terms[1].value)
                self.datapath.select_src_register(self.terms[2].value)
            else: 
                self.datapath.select_dst_register(self.terms[1].value)
        
        if self.opcode == Opcode.INC:
            if self.terms[0].value == 0:
                self.datapath.select_dst_register(self.terms[1].value)
                self.datapath.select_src_register(self.terms[1].value)

        ALU_operations = (Opcode.ADD, Opcode.SUB, Opcode.MUL,
                      Opcode.DIV, Opcode.RMD, Opcode.AND,
                      Opcode.OR, Opcode.EQ, Opcode.NEQ,
                      Opcode.LT, Opcode.GT)
        
        if self.opcode in ALU_operations:
            self.n = self.terms[1].value
            self.datapath.select_dst_register(self.terms[2].value)

        if self.opcode in (Opcode.BEQZ, Opcode.BNEZ, Opcode.BGZ, Opcode.BLZ):
            self.datapath.select_src_register(self.terms[1])
        
        if self.opcode in (Opcode.PUSH, Opcode.JMP, Opcode.CALL):
            if self.terms[1].value == 0:
                self.datapath.select_src_register(self.terms[2].value)
            

    def latch_program_counter(self, sel : Sel.ProgramCounter):
        assert isinstance(sel, Sel.ProgramCounter), "selector must be ProgramCounter selector"

        if sel == Sel.ProgramCounter.JUMP:
            pass
        if sel == Sel.ProgramCounter.NEXT:
            self.program_counter += 1

    def latch_mprogram_counter(self, sel: Sel.MProgramCounter):
        assert isinstance(sel, Sel.MProgramCounter), "selector must be MProgramCounter selector"

        if sel == Sel.MProgramCounter.ZERO:
            self.mprogram_counter = 0
        if sel == Sel.MProgramCounter.OPCODE:
            self.mprogram_counter = self.opcode.value
        if sel == Sel.MProgramCounter.TYPE:
            self.mprogram_counter += self.terms[1]

    def latch_instruction(self):
        self.decode(self.datapath.data_register)

    def latch_value_register(self):
        self.value_register = self.datapath.data_register

    




class DataPath:
    def __init__(self, input_address, output_address):
        self.control_unit : ControlUnit = ControlUnit(self)
        self.alu : ALU = ALU(self)
        self.registers : Registers = Registers()

        self.data_register : int = 0
        self.address_register : int = 0
        self.choose_register : Registers.Registers = None
        self.src_register : Registers.Registers = None
        self.dst_register : Registers.Registers = None

        self.input_address : int = input_address
        self.output_address : int = output_address

    def select_src_register(self, register : Registers.Registers):
        self.src_register = register

    def select_dst_register(self, register : Registers.Registers):
        self.dst_register = register

    def latch_data_register(self, sel : Sel.DataRegister):
        assert isinstance(sel, Sel.DataRegister), "selector must be DataRegister selector"

        if sel == Sel.DataRegister.ALU:
            self.data_register = self.alu.result
        elif sel == Sel.DataRegister.MEMORY:
            self.data_register = self.memory[self.address_register]
        
    def latch_address_register(self, sel : Sel.AddressRegister):
        assert isinstance(sel, Sel.AddressRegister), "selector must be AddressRegister selector"

        if sel == Sel.AddressRegister.CONTROL_UNIT:
            self.address_register = self.control_unit.program_counter
        elif sel == Sel.AddressRegister.REGISTER:
            self.address_register = self.registers[self.choose_register]
        elif sel == Sel.AddressRegister.STACK_POINTER_REGISTER: # TODO remove RSP 
            self.address_register = self.registers[Registers.Registers.RSP]

    def latch_register(self, sel : Sel.Register, register : Registers.Registers):
        assert isinstance(sel, Sel.Register), "selector must be Register selector"

        if sel == Sel.Register.ALU:
            self.registers[register] = self.alu.result
        elif sel == Sel.Register.DATA_REGISTER:
            self.registers[register] = self.data_register
        elif sel == Sel.Register.IMMEDIATE:
            self.registers[register] = self.control_unit.immediate
        elif sel == Sel.Register.REGISTER:
            self.registers[register] == self.registers[self.choose_register]

    # def read_from_memory(self) -> int:
    #     if self.address_register == self.input_address:
    #         pass
    #     else:
    #         return memory[self.address_register]




if __name__ == "__main__":
    instruction = Instruction(Opcode.MOV, [Term(0), Term(Registers.Registers.R0), Term(Registers.Registers.R1)])
    print(instruction)

    datapath = DataPath(100, 120)
    datapath.control_unit.decode(instruction)
    print(datapath.control_unit.terms, datapath.control_unit.opcode)
    print(datapath.src_register, datapath.dst_register)