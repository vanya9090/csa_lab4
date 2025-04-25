from enum import Enum 
from dataclasses import dataclass


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

