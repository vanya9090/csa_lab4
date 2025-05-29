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
    NADD_mem : int = 160
    NSUB_mem : int = 176
    NMUL_mem : int = 321
    NAND_mem : int = 208
    NOR_mem : int = 192
    BEQZ : int = 241
    BNEZ : int = 255
    BGZ : int = 269
    BLZ : int = 283
    PUSH : int = 18
    JMP_r : int = 224
    JMP_imm : int = 231
    POP : int = 21
    HLT : int = 23
    CALL : int = 297
    RET : int = 314
    LT : int = 0
    GT : int = 1
    EQ : int = 2
    ADD_reg2reg : int = 337
    ADD_mem2reg : int = ADD_reg2reg + 6
    ADD_mem2mem : int = ADD_mem2reg + 16
    ADD_mix2reg1 : int = ADD_mem2mem + 21
    ADD_mix2reg2 : int = ADD_mem2mem + 21

    SUB_reg2reg : int = 407
    SUB_mem2reg : int = SUB_reg2reg + 6
    SUB_mem2mem : int = SUB_mem2reg + 16
    SUB_mix2reg1 : int = SUB_mem2mem + 21
    SUB_mix2reg2 : int = SUB_mix2reg1 + 11

    MUL_reg2reg : int = SUB_mix2reg2 + 11
    MUL_mem2reg : int = MUL_reg2reg + 6
    MUL_mem2mem : int = MUL_mem2reg + 16
    MUL_mix2reg1 : int = MUL_mem2mem + 21
    MUL_mix2reg2 : int = MUL_mem2mem + 21

    DIV_reg2reg : int = MUL_mix2reg2 + 11
    DIV_mem2reg : int = DIV_reg2reg + 6
    DIV_mem2mem : int = DIV_mem2reg + 16
    DIV_mix2reg1 : int = DIV_mem2mem + 21
    DIV_mix2reg2 : int = DIV_mix2reg1 + 11

    RMD_reg2reg : int = DIV_mix2reg2 + 11
    RMD_mem2reg : int = RMD_reg2reg + 6
    RMD_mem2mem : int = RMD_mem2reg + 16
    RMD_mix2reg1 : int = RMD_mem2mem + 21
    RMD_mix2reg2 : int = RMD_mix2reg1 + 11

    AND_reg2reg : int = RMD_mix2reg2 + 11
    AND_mem2reg : int = AND_reg2reg + 6
    AND_mem2mem : int = AND_mem2reg + 16
    AND_mix2reg1 : int = AND_mem2mem + 21
    AND_mix2reg2 : int = AND_mem2mem + 21

    OR_reg2reg : int = AND_mix2reg2 + 11
    OR_mem2reg : int = OR_reg2reg + 6
    OR_mem2mem : int = OR_mem2reg + 16
    OR_mix2reg1 : int = OR_mem2mem + 21
    OR_mix2reg2 : int = OR_mem2mem + 21

    XOR_reg2reg : int = OR_mix2reg2 + 11
    XOR_mem2reg : int = XOR_reg2reg + 6
    XOR_mem2mem : int = XOR_mem2reg + 16
    XOR_mix2reg1 : int = XOR_mem2mem + 21
    XOR_mix2reg2 : int = XOR_mem2mem + 21

    MOV_mem2mem : int = 391

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
