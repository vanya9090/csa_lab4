from __future__ import annotations

import re
from typing import List, Union

from isa import Instruction, Opcode, Term
from machine import Registers


REG_RE = re.compile(r"R([0-7])\Z", re.IGNORECASE)


def _reg(token: str) -> Registers.Registers:
    m = REG_RE.fullmatch(token)
    if not m:
        raise ValueError(f"Unknown register {token!r}")
    return Registers.Registers(int(m.group(1)) + 3)  # R0 enum value is 3


def _parse(token: str):
    token = token.strip()
    if token.startswith("#"): # immediate
        return "imm", int(token[1:], 0)
    if token.startswith("[") and token.endswith("]"):
        inner = token[1:-1].strip()
        if REG_RE.fullmatch(inner): # [R?]  → reg indirect
            return "reg_ind", _reg(inner)
        return "indirect", int(inner, 0) # [addr]
    if REG_RE.fullmatch(token): # R?
        return "reg", _reg(token)
    return "direct", int(token, 0) # bare number = absolute addr


def assemble_line(src: str) -> List[Union[Instruction, int]]:
    src = src.partition(";")[0].strip()
    if not src:
        return []

    mnem, _, rest = src.partition(" ")
    mnem = mnem.upper()
    ops = [o.strip() for o in rest.split(",")] if rest else []

    if mnem == "MOV":
        if len(ops) != 2:
            raise SyntaxError("MOV needs 2 operands")
        dst_k, dst_v = _parse(ops[0])
        src_k, src_v = _parse(ops[1])

        if dst_k != "reg":
            raise SyntaxError("destination of MOV must be a register")

        if src_k == "reg":
            return [Instruction(Opcode.MOV, [Term(0), Term(dst_v), Term(src_v)])]
        if src_k == "reg_ind":
            return [Instruction(Opcode.MOV, [Term(7), Term(dst_v), Term(src_v)])]
        if src_k == "imm":
            return [Instruction(Opcode.MOV, [Term(17), Term(dst_v)]), src_v]
        if src_k == "direct":
            return [Instruction(Opcode.MOV, [Term(23), Term(dst_v)]), src_v]
        if src_k == "indirect":
            return [Instruction(Opcode.MOV, [Term(37), Term(dst_v)]), src_v]

    if mnem in ("INC", "DEC"):
        if len(ops) != 1:
            raise SyntaxError(f"{mnem} needs 1 operand")
        op_k, op_v = _parse(ops[0])

        opcode = Opcode.INC if mnem == "INC" else Opcode.DEC
        if op_k == "reg":
            return [Instruction(opcode, [Term(0), Term(op_v)])]
        if op_k in ("direct", "indirect"):
            return [Instruction(opcode, [Term(7)]), op_v]

    raise NotImplementedError(f"asm does not support '{mnem}'")


def assemble_program(source: str) -> List[Union[Instruction, int]]:
    program: List[Union[Instruction, int]] = []
    for line in source.splitlines():
        program.extend(assemble_line(line))
    return program
