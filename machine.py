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
