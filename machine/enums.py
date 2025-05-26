from enum import Enum 

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

class ALUOperations(Enum):
    ADD : int = 0
    SUB : int = 1
    AND : int = 2
    OR : int = 3
    MUL : int = 4
    DIV : int = 5
    RMD : int = 6
