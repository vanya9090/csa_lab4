from enum import Enum 
from dataclasses import dataclass
from typing import Callable, Dict, Any


class Signal(Enum):
    LATCH_ADDRESS_REGISTER : int = 0
    LATCH_DATA_REGISTER : int = 1
    LATCH_STACK_POINTER_REGISTER : int = 2
    
    LATCH_PROGRAMM_COUNTER : int = 3
    LATCH_MPROGRAMM_COUNTER : int = 4

    LATCH_LEFT_ALU : int = 5
    LATCH_RIGHT_ALU : int = 6

    LATCH_REGISTER : int = 7


class Sel:
    class DataRegister(Enum):
        MEMORY : int = 0
        ALU: int = 1
    class AddressRegister(Enum):
        CONTROL_UNIT : int = 0
        REGISTER :int = 1
        STACK_POINTER_REGISTER : int = 2
    class ProgramCounter(Enum):
        JUMP : int = 0
        NEXT : int = 1
    class MProgramCounter(Enum):
        OPCODE : int = 0
        NEXT : int = 1
    class LeftALU(Enum):
        REGISTER : int = 0
        IMMEDIATE : int = 1
    class RightALU(Enum):
        REGISTER : int = 0
        IMMEDIATE : int = 1
        DATA_REGISTER : int = 2
        PLUS_1 : int = 3
        MINUS_1 : int = 4
    class Register(Enum):
        REGISTER : int = 0
        IMMEDIATE : int = 1
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


    def __init__(self):
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
            pass
        if sel == Sel.LeftALU.IMMEDIATE:
            pass
    
    def latch_right_alu(self, sel : Sel.RightALU) -> None:
        assert isinstance(sel, Sel.RightALU), "selector must be RightALU selector"

        if sel == Sel.RightALU.REGISTER:
            pass
        if sel == Sel.RightALU.IMMEDIATE:
            pass
        if sel == Sel.RightALU.DATA_REGISTER:
            pass
        if sel == Sel.RightALU.PLUS_1:
            self.__right_term = 1
        if sel == Sel.RightALU.MINUS_1:
            self.__right_term = -1

    def perform(self, operation : Operations) -> None:
        self.result = self.__operations[operation](self.__left_term, self.__right_term)
        self.__set_flags()


class Memory:
    pass


class Registers:
    pass


class ControlUnit:
    pass


class DataPath:
    def __init__(self):
        self.control_unit : ControlUnit = ControlUnit()
        self.alu : ALU = ALU()
        self.registers : Registers = Registers()

        self.data_register : int = 0
        self.address_register : int = 0





if __name__ == "__main__":
    alu = ALU()
    print(alu.flags[alu.Flags.ZERO])