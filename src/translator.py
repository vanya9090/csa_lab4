from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from typing import Union, Any

from isa import Instruction, Opcode, Term
from machine.machine import Address, DataPath, Memory, Registers


@dataclass
class Number:
    value: int


@dataclass
class Symbol:
    value: str


@dataclass
class Atom:
    value: Number | Symbol


class Operation(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    RMD = "%"
    LT = "<"
    GT = ">"
    EQ = "=="
    NEQ = "!="
    AND = "&"
    OR = "|"
    XOR = "^"


class AddressingType(Enum):
    REG2REG = auto()
    MEM2REG = auto()
    MIX2REG1 = auto()
    MIX2REG2 = auto()
    MEM2MEM = auto()


@dataclass
class Exp:
    operation: Operation | Atom
    operands: list[Union[Atom, "Exp"]]


BINOP_OPCODE: dict[Operation, dict[AddressingType, Opcode]] = {
    Operation.ADD: {
        AddressingType.MEM2MEM: Opcode.ADD_mem2mem,
        AddressingType.REG2REG: Opcode.ADD_reg2reg,
        AddressingType.MEM2REG: Opcode.ADD_mem2reg,
        AddressingType.MIX2REG1: Opcode.ADD_mix2reg1,
        AddressingType.MIX2REG2: Opcode.ADD_mix2reg2,
    },
    Operation.SUB: {
        AddressingType.MEM2MEM: Opcode.SUB_mem2mem,
        AddressingType.REG2REG: Opcode.SUB_reg2reg,
        AddressingType.MEM2REG: Opcode.SUB_mem2reg,
        AddressingType.MIX2REG1: Opcode.SUB_mix2reg1,
        AddressingType.MIX2REG2: Opcode.SUB_mix2reg2,
    },
    Operation.MUL: {
        AddressingType.MEM2MEM: Opcode.MUL_mem2mem,
        AddressingType.REG2REG: Opcode.MUL_reg2reg,
        AddressingType.MEM2REG: Opcode.MUL_mem2reg,
        AddressingType.MIX2REG1: Opcode.MUL_mix2reg1,
        AddressingType.MIX2REG2: Opcode.MUL_mix2reg2,
    },
    Operation.DIV: {
        AddressingType.MEM2MEM: Opcode.DIV_mem2mem,
        AddressingType.REG2REG: Opcode.DIV_reg2reg,
        AddressingType.MEM2REG: Opcode.DIV_mem2reg,
        AddressingType.MIX2REG1: Opcode.DIV_mix2reg1,
        AddressingType.MIX2REG2: Opcode.DIV_mix2reg2,
    },
    Operation.RMD: {
        AddressingType.MEM2MEM: Opcode.RMD_mem2mem,
        AddressingType.REG2REG: Opcode.RMD_reg2reg,
        AddressingType.MEM2REG: Opcode.RMD_mem2reg,
        AddressingType.MIX2REG1: Opcode.RMD_mix2reg1,
        AddressingType.MIX2REG2: Opcode.RMD_mix2reg2,
    },
    Operation.AND: {
        AddressingType.MEM2MEM: Opcode.AND_mem2mem,
        AddressingType.REG2REG: Opcode.AND_reg2reg,
        AddressingType.MEM2REG: Opcode.AND_mem2reg,
        AddressingType.MIX2REG1: Opcode.AND_mix2reg1,
        AddressingType.MIX2REG2: Opcode.AND_mix2reg2,
    },
    Operation.OR: {
        AddressingType.MEM2MEM: Opcode.OR_mem2mem,
        AddressingType.REG2REG: Opcode.OR_reg2reg,
        AddressingType.MEM2REG: Opcode.OR_mem2reg,
        AddressingType.MIX2REG1: Opcode.OR_mix2reg1,
        AddressingType.MIX2REG2: Opcode.OR_mix2reg2,
    },
    Operation.XOR: {
        AddressingType.MEM2MEM: Opcode.XOR_mem2mem,
        AddressingType.REG2REG: Opcode.XOR_reg2reg,
        AddressingType.MEM2REG: Opcode.XOR_mem2reg,
        AddressingType.MIX2REG1: Opcode.XOR_mix2reg1,
        AddressingType.MIX2REG2: Opcode.XOR_mix2reg2,
    },
}

COMPARE_OPCODE: dict[Operation, Opcode] = {
    Operation.LT: Opcode.BLZ,
    Operation.GT: Opcode.BGZ,
    Operation.EQ: Opcode.BEQZ,
    Operation.NEQ: Opcode.BNEZ,
}


# первоначальный этап обработки программы на LISP
class Tokenizer:
    def tokenize(self, s: str) -> list[str]:
        return s.replace("(", " ( ").replace(")", " ) ").split()


# создание AST
class Parser:
    def parse(self, tokens: list[str]) -> Exp | Atom:
        if not tokens:
            err_message = "unexpected EOF"
            raise SyntaxError(err_message)

        token = tokens.pop(0)

        if token == "(":
            if not tokens:
                err_message = 'missing operation after "("'
                raise SyntaxError(err_message)
            op_token = tokens.pop(0)
            try:
                op = Operation(op_token)
            except ValueError:
                op = self.atom(op_token)

            args = []
            while tokens[0] != ")":
                args.append(self.parse(tokens))
            tokens.pop(0)  # remove ')'
            return Exp(operation=op, operands=args)

        if token == ")":
            err_message = "unexpected ')'"
            raise SyntaxError(err_message)
        return self.atom(token)

    def atom(self, token: str) -> Atom:
        try:
            return Atom(Number(int(token)))
        except ValueError:
            return Atom(Symbol(token))


class Program:
    def __init__(self, memory: Memory):
        self.memory = memory
        self.idx = 0


# генерация asm кода из AST
class Generator:
    def __init__(
        self,
        var_allocator: "VariableAllocator",
        reg_controller: "RegisterController",
        program: Program,
    ):
        self.handlers_map: dict[str, Callable[[list[Any]], None]] = {
            "begin": self.handle_begin,
            "setq": self.handle_setq,
            "binop": self.handle_binop,
            # 'defun': self.handle_defun,
            "while": self.handle_while,
            "cond": self.handle_cond,
        }
        self.var_allocator = var_allocator
        self.reg_controller = reg_controller
        self.program = program
        self.PC = 0

    def generate(self, expression: Exp | Atom) -> Address | Registers.Registers | None:
        if isinstance(expression, Atom):
            return self.handle_atom(expression)
        if isinstance(expression, Exp):
            op = expression.operation
            if isinstance(op, Operation):
                return self.handlers_map["binop"](op, expression.operands)
            if isinstance(op, Atom):
                return self.handlers_map[op.value.value](expression.operands)
        err_message = f"operation: f{op}"
        raise RuntimeError(err_message)

    def handle_begin(self, operands: list[Exp]) -> None:
        [self.generate(operand) for operand in operands]

    def handle_atom(self, atom: Atom) -> Address | Registers.Registers:
        if isinstance(atom.value, Symbol):
            return self.var_allocator.allocate(atom.value.value)
        if isinstance(atom.value, Number):
            reg = self.reg_controller.alloc()
            self.program.memory[Address(self.PC)] = Instruction(
                Opcode.MOV_imm2r,
                [Term(reg)],
            )
            self.program.memory[Address(self.PC + 1)] = atom.value.value
            self.PC += 2
            return reg
        err_message = f"Atom {atom} isn't atom"
        raise RuntimeError(err_message)

    def handle_binop(
        self, operation: Operation, operands: list[Exp],
    ) -> Registers.Registers:
        first = self.generate(operands[0])
        second = self.generate(operands[1])
        dst_reg = self.reg_controller.alloc()

        if operation in (Operation.LT, Operation.GT, Operation.EQ, Operation.NEQ):
            operation = Operation.SUB
            first, second = second, first

        if isinstance(first, Registers.Registers):
            if isinstance(second, Registers.Registers):
                self.program.memory[Address(self.PC)] = Instruction(
                    BINOP_OPCODE[operation][AddressingType.REG2REG],
                    [Term(dst_reg), Term(first), Term(second)],
                )
                self.PC += 1

                self.reg_controller.release(first)
                self.reg_controller.release(second)

            elif isinstance(second, Address):
                self.program.memory[Address(self.PC)] = Instruction(
                    BINOP_OPCODE[operation][AddressingType.MIX2REG1],
                    [Term(dst_reg), Term(first)],
                )
                self.program.memory[Address(self.PC + 1)] = second.value
                self.PC += 2

                self.reg_controller.release(first)

        elif isinstance(first, Address):
            if isinstance(second, Address):
                self.program.memory[Address(self.PC)] = Instruction(
                    BINOP_OPCODE[operation][AddressingType.MEM2REG],
                    [Term(dst_reg)],
                )
                self.program.memory[Address(self.PC + 1)] = first.value
                self.program.memory[Address(self.PC + 2)] = second.value
                self.PC += 3

            elif isinstance(second, Registers.Registers):
                self.program.memory[Address(self.PC)] = Instruction(
                    BINOP_OPCODE[operation][AddressingType.MIX2REG2],
                    [Term(dst_reg), Term(second)],
                )
                self.program.memory[Address(self.PC + 1)] = first.value
                self.PC += 2

                self.reg_controller.release(second)

        return dst_reg

    def handle_setq(self, operands: list[Exp]) -> Address:
        var_address: Address = self.generate(operands[0])
        var_value: Registers.Registers | Address = self.generate(operands[1])

        if isinstance(var_value, Address):
            self.program.memory[Address(self.PC)] = Instruction(Opcode.MOV_mem2mem, [])
            self.program.memory[Address(self.PC + 1)] = var_value.value
            self.program.memory[Address(self.PC + 2)] = var_address.value
            self.PC += 3

        elif isinstance(var_value, Registers.Registers):
            self.program.memory[Address(self.PC)] = Instruction(
                Opcode.STORE_r2da,
                [Term(var_value)],
            )
            self.program.memory[Address(self.PC + 1)] = var_address.value

            self.PC += 2
            self.reg_controller.release(var_value)

        return var_address

    # def _extract_cmp_op() ->

    def handle_while(self, operands: list[Exp]) -> None:
        start_pc = self.PC
        cond_reg = self.generate(operands[0])
        self.program.memory[Address(self.PC)] = Instruction(
            COMPARE_OPCODE[operands[0].operation],
            [Term(cond_reg)],
        )
        self.program.memory[Address(self.PC + 1)] = None  # placeholder
        jmp_pc = self.PC + 1
        self.PC += 2

        # generate loop body
        [self.generate(operand) for operand in operands[1:]]

        self.program.memory[Address(self.PC)] = Instruction(Opcode.JMP_imm, [])
        self.program.memory[Address(self.PC + 1)] = start_pc

        self.PC += 2
        self.program.memory[Address(jmp_pc)] = self.PC

    def handle_cond(self, operands: list[Exp]) -> None:
        for i, op in enumerate(operands):
            if i % 2 == 0:
                cond_reg = self.generate(op)
                self.program.memory[Address(self.PC)] = Instruction(
                    COMPARE_OPCODE[op.operation],
                    [Term(cond_reg)],
                )
                self.program.memory[Address(self.PC + 1)] = None  # placeholder
                jmp_pc = self.PC + 1
                self.PC += 2
            else:
                self.generate(op)
                self.program.memory[Address(jmp_pc)] = self.PC

    # def handle_defun(self, operands : list[Exp]) -> None:


class RegisterController:
    def __init__(self):
        self.available = [3, 4, 5, 6, 7, 8, 9, 10]

    def alloc(self) -> Registers.Registers:
        print(self.available)
        return Registers.Registers(self.available.pop())

    def release(self, reg: Registers.Registers) -> None:
        self.available.append(reg.value)


class VariableAllocator:
    def __init__(self, base_address: int = 1000):
        self.var_map: dict[str, Address] = {}
        self.next_free_address = base_address

    def allocate(self, varname: str) -> Address:
        if varname in self.var_map:
            return self.var_map[varname]
        addr = Address(self.next_free_address)
        self.var_map[varname] = addr
        self.next_free_address += 1
        return addr

    def __getitem__(self, varname: str) -> int:
        return self.var_map[varname]

    def __setitem__(self, varname: str, address: int) -> None:
        self.var_map[varname] = address


# TODO fix scopes parser: if (( or )) work incorrect
if __name__ == "__main__":
    reg_controller = RegisterController()
    var_allocator = VariableAllocator()

    expression = """
    (begin
        (cond (< 3 3) (begin (setq i 1))
              (> 3 3) (begin (setq j 1))
        )
    )
"""
    # expression = """(+ 1 (* 2 3))"""
    # expression = """
    # (begin
    #     (setq i 0)
    #     (setq n 3)
    #     (setq sum 0)
    #     (setq sum2 0)
    #     (while (< i n)
    #         (setq sum (+ sum i))
    #         (setq sum2 (+ sum2 (* i i)))
    #         (setq i (+ i 1))
    #     )
    #     (setq sum (* sum sum))
    #     (setq res (- sum sum2))
    # )
    # """
    #     expression = """
    # (begin
    #     (setq n 10)
    #     (setq sum 0)
    #     (setq sum2 0)
    #     (setq i 0)
    #     (while (< i n)
    #         (setq sum (+ sum i))
    #         (setq sum2 (+ sum2 (* i i)))
    #         (setq i (+ i 1))
    #     )
    #     (setq num (+ 1 2))
    # )
    #     """
    dp = DataPath(input_address=0, output_address=0)

    memory = dp.memory
    program = Program(memory)

    tokenizer = Tokenizer()
    parser = Parser()
    generator = Generator(var_allocator, reg_controller, program)
    print(tokenizer.tokenize(expression))
    print(parser.parse(tokenizer.tokenize(expression)))
    print()
    print(
        generator.generate(
            parser.parse(tokenizer.tokenize(expression)),
        ),
    )
    print()
    inv_var_map = {v.value: k for k, v in var_allocator.var_map.items()}
    for i in range(40):
        if isinstance(memory[Address(i)], Instruction):
            print(f"{i}: {memory[Address(i)]}")
        elif memory[Address(i)] in inv_var_map:
            print(f"{i}({inv_var_map[memory[Address(i)]]}): {memory[Address(i)]}")
        else:
            print(f"{i}: {memory[Address(i)]}")
    print("\n")
    print(f"PC: {generator.PC}")
    dp.program_counter = 0
    MAX_CYCLES = 100_000
    for cycle in range(MAX_CYCLES):
        dp.control_unit.run_single_micro()
        if dp.program_counter >= generator.PC:
            print(f"\nProgram finished after {cycle + 1} micro-cycles.")
            break
    else:
        print("cycle limit hit")

    print("\nRegister file:")
    for r, v in dp.registers.registers_value.items():
        print(f"  {r.name:3} = {v}")

    print()
    inv_var_map = {v.value: k for k, v in var_allocator.var_map.items()}
    for i in range(1000, 1010):
        if isinstance(memory[Address(i)], Instruction):
            print(f"{i}: {memory[Address(i)]}")
        elif memory[Address(i)] in inv_var_map:
            print(f"{i}({inv_var_map[memory[Address(i)]]}): {memory[Address(i)]}")
        else:
            print(f"{i}: {memory[Address(i)]}")
    print("\n")
