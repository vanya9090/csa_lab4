from enum import Enum 
from dataclasses import dataclass
from typing import Any

class Opcode(Enum):
    MOV : int = 0
    INC : int = 1
    DEC : int = 2
    ADD : int = 3
    SUB : int = 4
    MUL : int = 5
    DIV : int = 6
    RMD : int = 7
    AND : int = 8
    OR : int = 9
    EQ : int = 10
    NEQ : int = 11
    LT : int = 12
    GT : int = 13
    BEQZ : int = 14
    BNEZ : int = 15
    BGZ : int = 16
    BLZ : int = 17
    PUSH : int = 18
    JMP : int = 19
    CALL : int = 20
    POP : int = 21
    RET : int = 22
    HLT : int = 23

# class TermType(Enum):
#     REGISTER : int = 0
#     REGISTER_INDIRECT : int = 1
#     IMMEDIATE : int = 2
#     DIRECT : int = 3
#     INDIRECT : int = 4

@dataclass
class Term:
    value : Any
    # term_type: TermType

@dataclass
class Instruction:
    opcode : Opcode
    terms: list[Term]
