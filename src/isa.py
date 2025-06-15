from dataclasses import dataclass
from enum import Enum
from typing import Any


class Opcode(Enum):
    MOV_r2r: int = 4
    MOV_rd2r: int = 10
    MOV_imm2r: int = 20
    MOV_da2r: int = 26
    MOV_ia2r: int = 40
    INC_r: int = 59
    INC_mem: int = 65
    DEC_r: int = 80
    DEC_mem: int = 86
    STORE_r2rd: int = 101
    STORE_r2ri: int = 112
    STORE_r2da: int = 128
    STORE_r2ia: int = 142
    NADD_mem: int = 161
    NSUB_mem: int = 177
    NMUL_mem: int = 325
    NAND_mem: int = 209
    NOR_mem: int = 193
    BEQZ: int = 242
    BNEZ: int = 256
    BGZ: int = 270
    BLZ: int = 284
    JMP_r: int = 225
    JMP_imm: int = 232
    CALL: int = 298
    RET: int = 315
    LT: int = 0
    GT: int = 1
    EQ: int = 2
    ADD_reg2reg: int = 337 + 4
    ADD_mem2reg: int = ADD_reg2reg + 6
    ADD_mem2mem: int = ADD_mem2reg + 16
    ADD_mix2reg1: int = ADD_mem2mem + 21
    ADD_mix2reg2: int = ADD_mem2mem + 21

    SUB_reg2reg: int = 407 + 4
    SUB_mem2reg: int = SUB_reg2reg + 6
    SUB_mem2mem: int = SUB_mem2reg + 16
    SUB_mix2reg1: int = SUB_mem2mem + 21
    SUB_mix2reg2: int = SUB_mix2reg1 + 11

    MUL_reg2reg: int = SUB_mix2reg2 + 11
    MUL_mem2reg: int = MUL_reg2reg + 6
    MUL_mem2mem: int = MUL_mem2reg + 16
    MUL_mix2reg1: int = MUL_mem2mem + 21
    MUL_mix2reg2: int = MUL_mem2mem + 21

    DIV_reg2reg: int = MUL_mix2reg2 + 11
    DIV_mem2reg: int = DIV_reg2reg + 6
    DIV_mem2mem: int = DIV_mem2reg + 16
    DIV_mix2reg1: int = DIV_mem2mem + 21
    DIV_mix2reg2: int = DIV_mix2reg1 + 11

    RMD_reg2reg: int = DIV_mix2reg2 + 11
    RMD_mem2reg: int = RMD_reg2reg + 6
    RMD_mem2mem: int = RMD_mem2reg + 16
    RMD_mix2reg1: int = RMD_mem2mem + 21
    RMD_mix2reg2: int = RMD_mix2reg1 + 11

    AND_reg2reg: int = RMD_mix2reg2 + 11
    AND_mem2reg: int = AND_reg2reg + 6
    AND_mem2mem: int = AND_mem2reg + 16
    AND_mix2reg1: int = AND_mem2mem + 21
    AND_mix2reg2: int = AND_mem2mem + 21

    OR_reg2reg: int = AND_mix2reg2 + 11
    OR_mem2reg: int = OR_reg2reg + 6
    OR_mem2mem: int = OR_mem2reg + 16
    OR_mix2reg1: int = OR_mem2mem + 21
    OR_mix2reg2: int = OR_mem2mem + 21

    XOR_reg2reg: int = OR_mix2reg2 + 11
    XOR_mem2reg: int = XOR_reg2reg + 6
    XOR_mem2mem: int = XOR_mem2reg + 16
    XOR_mix2reg1: int = XOR_mem2mem + 21
    XOR_mix2reg2: int = XOR_mem2mem + 21

    MOV_mem2mem: int = 391 + 4

    PUSH: int = XOR_mix2reg2 + 11
    POP: int = PUSH + 9
    HLT: int = POP + 6


OPCODE_TO_TERMS_AMOUNT: dict[Opcode, list[int]] = {
    Opcode.MOV_r2r        : [2, 0],
    Opcode.MOV_rd2r       : [1, 1],
    Opcode.MOV_imm2r      : [1, 1],
    Opcode.MOV_da2r       : [1, 1],
    Opcode.MOV_ia2r       : [1, 1],

    Opcode.INC_r          : [1, 0],
    Opcode.INC_mem        : [0, 1],
    Opcode.DEC_r          : [1, 0],
    Opcode.DEC_mem        : [0, 1],

    Opcode.STORE_r2rd     : [2, 0],
    Opcode.STORE_r2ri     : [2, 0],
    Opcode.STORE_r2da     : [1, 1],
    Opcode.STORE_r2ia     : [1, 1],

    Opcode.NADD_mem       : [1, 2],
    Opcode.NSUB_mem       : [1, 2],
    Opcode.NMUL_mem       : [1, 2],
    Opcode.NAND_mem       : [1, 2],
    Opcode.NOR_mem        : [1, 2],

    Opcode.BEQZ           : [1, 1],
    Opcode.BNEZ           : [1, 1],
    Opcode.BGZ            : [1, 1],
    Opcode.BLZ            : [1, 1],
    Opcode.JMP_r          : [1, 0],
    Opcode.JMP_imm        : [0, 1],

    Opcode.CALL           : [0, 1],
    Opcode.RET            : [0, 0],
    Opcode.PUSH           : [1, 0],
    Opcode.POP            : [1, 0],

    Opcode.ADD_reg2reg    : [3, 0],
    Opcode.SUB_reg2reg    : [3, 0],
    Opcode.MUL_reg2reg    : [3, 0],
    Opcode.DIV_reg2reg    : [3, 0],
    Opcode.RMD_reg2reg    : [3, 0],
    Opcode.AND_reg2reg    : [3, 0],
    Opcode.OR_reg2reg     : [3, 0],
    Opcode.XOR_reg2reg    : [3, 0],

    Opcode.ADD_mem2reg    : [1, 2],
    Opcode.SUB_mem2reg    : [1, 2],
    Opcode.MUL_mem2reg    : [1, 2],
    Opcode.DIV_mem2reg    : [1, 2],
    Opcode.RMD_mem2reg    : [1, 2],
    Opcode.AND_mem2reg    : [1, 2],
    Opcode.OR_mem2reg     : [1, 2],
    Opcode.XOR_mem2reg    : [1, 2],

    Opcode.ADD_mem2mem    : [0, 3],
    Opcode.SUB_mem2mem    : [0, 3],
    Opcode.MUL_mem2mem    : [0, 3],
    Opcode.DIV_mem2mem    : [0, 3],
    Opcode.RMD_mem2mem    : [0, 3],
    Opcode.AND_mem2mem    : [0, 3],
    Opcode.OR_mem2mem     : [0, 3],
    Opcode.XOR_mem2mem    : [0, 3],

    Opcode.ADD_mix2reg1   : [2, 1],
    Opcode.SUB_mix2reg1   : [2, 1],
    Opcode.MUL_mix2reg1   : [2, 1],
    Opcode.DIV_mix2reg1   : [2, 1],
    Opcode.RMD_mix2reg1   : [2, 1],
    Opcode.AND_mix2reg1   : [2, 1],
    Opcode.OR_mix2reg1    : [2, 1],
    Opcode.XOR_mix2reg1   : [2, 1],

    Opcode.ADD_mix2reg2   : [2, 1],
    Opcode.SUB_mix2reg2   : [2, 1],
    Opcode.MUL_mix2reg2   : [2, 1],
    Opcode.DIV_mix2reg2   : [2, 1],
    Opcode.RMD_mix2reg2   : [2, 1],
    Opcode.AND_mix2reg2   : [2, 1],
    Opcode.OR_mix2reg2    : [2, 1],
    Opcode.XOR_mix2reg2   : [2, 1],

    Opcode.MOV_mem2mem    : [0, 2],
    Opcode.HLT            : [0, 0],
}



@dataclass
class Term:
    value: Any
    # term_type: TermType


@dataclass
class Instruction:
    opcode: Opcode
    terms: list[Term]

