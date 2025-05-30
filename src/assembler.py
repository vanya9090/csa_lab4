from __future__ import annotations

import re
from typing import List, Union

from isa import Instruction, Opcode, Term
from machine.machine import Registers


REG_RE = re.compile(r"(RSP|R[0-7])\Z", re.IGNORECASE)


def _reg(token: str) -> Registers.Registers:
    m = REG_RE.fullmatch(token)
    if not m:
        raise ValueError(f"Unknown register {token!r}")
    token = token.upper()
    if token == "RSP":
        return Registers.Registers.RSP
    return Registers.Registers[f"R{token[1]}"]



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
            return [Instruction(Opcode.MOV_r2r, [Term(dst_v), Term(src_v)])]
        if src_k == "reg_ind":
            return [Instruction(Opcode.MOV_rd2r, [Term(dst_v), Term(src_v)])]
        if src_k == "imm":
            return [Instruction(Opcode.MOV_imm2r, [Term(dst_v)]), src_v]
        if src_k == "direct":
            return [Instruction(Opcode.MOV_da2r, [Term(dst_v)]), src_v]
        if src_k == "indirect":
            return [Instruction(Opcode.MOV_ia2r, [Term(dst_v)]), src_v]
    
    if mnem == "STORE":
        if len(ops) != 2:
            raise SyntaxError("STORE needs 2 operands")

        src_k, src_v = _parse(ops[0])
        dst_k, dst_v = _parse(ops[1])

        if src_k != "reg":
            raise SyntaxError("source of STORE must be a register")

        if dst_k == "reg":
            return [Instruction(Opcode.STORE_r2rd, [Term(src_v), Term(dst_v)])]
        if dst_k == "reg_ind":
            return [Instruction(Opcode.STORE_r2ri, [Term(src_v), Term(dst_v)])]
        if dst_k == "direct":
            return [Instruction(Opcode.STORE_r2da, [Term(src_v)]), dst_v]
        if dst_k == "indirect":
            return [Instruction(Opcode.STORE_r2imm, [Term(src_v)]), dst_v]

        raise SyntaxError("invalid destination in STORE")


    if mnem in ("INC", "DEC"):
        if len(ops) != 1:
            raise SyntaxError(f"{mnem} needs 1 operand")
        op_k, op_v = _parse(ops[0])

        if op_k == "reg":
            return [Instruction(Opcode.INC_r if mnem == "INC" else Opcode.DEC_r, [Term(op_v)])]
        if op_k == "direct":
            return [Instruction(Opcode.INC_mem if mnem == "INC" else Opcode.DEC_mem, []), op_v]

    if mnem == "ADD":
        if len(ops) < 2:
            raise SyntaxError("ADD needs at least two operands (N and destination register)")
        try:
            n = int(ops[0], 0)
        except ValueError:
            raise SyntaxError("First operand of ADD must be an integer constant (N)")

        dst_k, dst_v = _parse(ops[1])
        if dst_k != "reg":
            raise SyntaxError("Second operand of ADD must be a destination register")

        addresses = []
        for token in ops[2:]:
            addr_k, addr_v = _parse(token)
            if addr_k != "direct":
                raise SyntaxError("ADD currently only supports direct addressing for source values")
            addresses.append(addr_v)

        if len(addresses) != n:
            raise SyntaxError(f"ADD expects {n} addresses, but got {len(addresses)}")

        return [Instruction(Opcode.ADD_mem, [Term(n), Term(dst_v)])] + addresses
    
    if mnem == "JMP":
        if len(ops) != 1:
            raise SyntaxError("JMP needs 1 operand")
        op_k, op_v = _parse(ops[0])
        if op_k == "reg":
            return [Instruction(Opcode.JMP_r, [Term(op_v)])]
        if op_k == "direct":
            return [Instruction(Opcode.JMP_imm, []), op_v]
        raise SyntaxError("JMP operand must be a register or direct address")

    if mnem in ("BEQZ", "BNEZ", "BGZ", "BLZ"):
        if len(ops) != 2:
            raise SyntaxError(f"{mnem} needs 2 operands")
        reg_k, reg_v = _parse(ops[0])
        addr_k, addr_v = _parse(ops[1])

        if reg_k != "reg":
            raise SyntaxError(f"First operand of {mnem} must be a register")
        if addr_k != "direct":
            raise SyntaxError(f"Second operand of {mnem} must be a direct address")

        opcode = {
            "BEQZ": Opcode.BEQZ,
            "BNEZ": Opcode.BNEZ,
            "BGZ": Opcode.BGZ,
            "BLZ": Opcode.BLZ,
        }[mnem]

        return [Instruction(opcode, [Term(reg_v)]), addr_v]
    
    if mnem == "CALL":
        if len(ops) != 1:
            raise SyntaxError("CALL needs 1 operand")
        op_k, op_v = _parse(ops[0])
        if op_k == "reg":
            return [Instruction(Opcode.CALL, [Term(op_v)])]
        if op_k == "direct":
            return [Instruction(Opcode.CALL, []), op_v]
        raise SyntaxError("CALL operand must be a register or direct address")

    if mnem == "RET":
        if len(ops) != 0:
            raise SyntaxError("RET takes no operands")
        return [Instruction(Opcode.RET, [])]


    raise NotImplementedError(f"asm does not support '{mnem}'")


def assemble_program(source: str) -> List[Union[Instruction, int]]:
    program: List[Union[Instruction, int]] = []
    for line in source.splitlines():
        program.extend(assemble_line(line))
    return program
