from enum import Enum 
from dataclasses import dataclass
from typing import Any

class Opcode(Enum):
    MOV_r2r : int = 4
    MOV_rd2r : int = 10
    MOV_imm2r : int = 20
    MOV_da2r : int = 26
    MOV_ia2r : int = 40
    INC_r : int = 58
    INC_mem : int = 64
    DEC_r : int = 79
    DEC_mem : int = 85
    STORE_r2rd : int = 100
    STORE_r2ri : int = 111
    STORE_r2da : int = 127
    STORE_r2ia : int = 141
    ADD_mem : int = 160
    SUB_mem : int = 176
    MUL_mem : int = 5
    DIV_mem : int = 6
    RMD_mem : int = 7
    AND_mem : int = 208
    OR_mem : int = 192
    EQ_mem : int = 10
    NEQ_mem : int = 11
    LT_mem : int = 12
    GT_mem : int = 13
    BEQZ : int = 241
    BNEZ : int = 255
    BGZ : int = 269
    BLZ : int = 283
    PUSH : int = 18
    JMP_r : int = 224
    JMP_imm : int = 231
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
