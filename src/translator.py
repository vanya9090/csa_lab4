from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum, auto
from typing import Union

from isa import Instruction, Opcode, Term
from machine import Address, DataPath, Memory, Registers, from_bytes


@dataclass
class Number:
    value: int


@dataclass
class Symbol:
    value: str


@dataclass
class Atom:
    value: Number | Symbol

    def as_symbol(self) -> str:
        if isinstance(self.value, Symbol):
            return self.value.value
        err_message = "expected Symbol, got Number"
        raise TypeError(err_message)


class Operation(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    RMD = "%"
    LT = "<="
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


class Tokenizer:
    def tokenize(self, s: str) -> list[str]:
        return s.replace("(", " ( ").replace(")", " ) ").split()


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
            op: Operation | Atom
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


class Generator:
    def __init__(
        self,
        var_allocator: "VariableAllocator",
        reg_controller: "RegisterController",
        program: list[Instruction | int],
    ):
        self.handlers_map: dict[str, Callable[[list[Exp]], Address | None]] = {
            "begin": self.handle_begin,
            "setq": self.handle_setq,
            "defun": self.handle_defun,
            "while": self.handle_while,
            "cond": self.handle_cond,
        }
        self.var_allocator = var_allocator
        self.reg_controller = reg_controller
        self.program = program
        self.PC = 0
        self.label_map: dict[str, dict[str: Address | int]] = {}

    def generate(self, expression: Exp | Atom) -> Address | Registers.Registers | None:
        if isinstance(expression, Atom):
            return self.handle_atom(expression)
        if isinstance(expression, Exp):
            op = expression.operation
            if isinstance(op, Operation):
                return self.handle_binop(op, expression.operands)
            if isinstance(op, Atom):
                if op.value.value in self.handlers_map:
                    return self.handlers_map[op.as_symbol()](expression.operands)
                return self.handle_call(op, expression.operands)

        err_message = f"operation: f{op}"
        raise RuntimeError(err_message)

    # def emit(self, opcode: Opcode, terms: list[Term], imm_terms: list[int | None]) -> None:
    #     self.program.memory[Address(self.PC)] = Instruction(opcode, terms)
    #     self.PC += 1
    #     for imm in imm_terms:
    #         self.program.memory[Address(self.PC)] = imm
    #         self.PC += 1

    def emit(self, opcode: Opcode, terms: list[Term], imm_terms: list[int | None]) -> None:
        self.program[self.PC] = Instruction(opcode, terms)
        self.PC += 1
        for imm in imm_terms:
            self.program[self.PC] = imm
            self.PC += 1

    def handle_begin(self, operands: list[Exp]) -> None:
        for operand in operands[:-1]:
            value = self.generate(operand)
            if isinstance(value, Registers.Registers):
                self.reg_controller.release(value)
        return self.generate(operands[-1])

    def handle_atom(self, atom: Atom) -> Address | Registers.Registers:
        if isinstance(atom.value, Symbol):
            return self.var_allocator.allocate(atom.value.value)
        if isinstance(atom.value, Number):
            dst_reg = self.reg_controller.alloc()
            self.emit(Opcode.MOV_imm2r, [Term(dst_reg)], [atom.value.value])
            return dst_reg
        err_message = f"Atom {atom} isn't atom"
        raise RuntimeError(err_message)

    def handle_binop(
        self,
        operation: Operation,
        operands: list[Atom | Exp],
    ) -> Registers.Registers:
        first = self.generate(operands[0])
        second = self.generate(operands[1])
        dst_reg = self.reg_controller.alloc()

        if operation in (Operation.LT, Operation.GT, Operation.EQ, Operation.NEQ):
            operation = Operation.SUB
            first, second = second, first

        if isinstance(first, Registers.Registers):
            if isinstance(second, Registers.Registers):
                self.emit(BINOP_OPCODE[operation][AddressingType.REG2REG], [Term(dst_reg), Term(first), Term(second)], [])
                self.reg_controller.release(first)
                self.reg_controller.release(second)

            elif isinstance(second, Address):
                self.emit(BINOP_OPCODE[operation][AddressingType.MIX2REG1], [Term(dst_reg), Term(first)], [second.value])
                self.reg_controller.release(first)

        elif isinstance(first, Address):
            if isinstance(second, Address):
                self.emit(BINOP_OPCODE[operation][AddressingType.MEM2REG], [Term(dst_reg)], [first.value, second.value])

            elif isinstance(second, Registers.Registers):
                self.emit(BINOP_OPCODE[operation][AddressingType.MIX2REG2], [Term(dst_reg), Term(second)], [first.value])
                self.reg_controller.release(second)

        return dst_reg

    def handle_setq(self, operands: list[Exp]) -> Address:
        var_address = self.generate(operands[0])
        assert var_address is not None
        assert isinstance(var_address, Address)

        var_value = self.generate(operands[1])
        assert var_value is not None
        assert isinstance(var_value, Registers.Registers | Address)

        if isinstance(var_value, Address):
            self.emit(Opcode.MOV_mem2mem, [], [var_value.value, var_address.value])

        elif isinstance(var_value, Registers.Registers):
            self.emit(Opcode.STORE_r2da, [Term(var_value)], [var_address.value])
            self.reg_controller.release(var_value)

        return var_address

    def handle_while(self, operands: list[Exp]) -> None:
        assert isinstance(operands[0].operation, Operation)

        start_pc = self.PC
        cond_reg = self.generate(operands[0])
        jmp_pc = self.PC + 1
        self.emit(COMPARE_OPCODE[operands[0].operation], [Term(cond_reg)], [None])
        self.reg_controller.release(cond_reg)

        # generate loop body
        for operand in operands[1:]:
            value = self.generate(operand)
            if isinstance(value, Registers.Registers):
                self.reg_controller.release(value)

        self.emit(Opcode.JMP_imm, [], [start_pc])
        self.program.memory[jmp_pc] = self.PC

    def handle_cond(self, operands: list[Exp]) -> Registers.Registers:
        dst_reg = self.reg_controller.alloc()
        for i, op in enumerate(operands):
            if i % 2 == 0:
                cond_reg = self.generate(op)
                jmp_pc = self.PC + 1
                self.emit(COMPARE_OPCODE[op.operation], [Term(cond_reg)], [None])
                self.reg_controller.release(cond_reg)
            else:
                tmp = self.generate(op)
                if isinstance(tmp, Registers.Registers):
                    self.emit(Opcode.MOV_r2r, [Term(dst_reg), Term(tmp)], [])
                    self.reg_controller.release(tmp)
                elif isinstance(tmp, Address):
                    self.emit(Opcode.MOV_da2r, [Term(dst_reg)], [tmp.value])
                self.program[jmp_pc] = self.PC

        return dst_reg

    def handle_defun(self, operands: list[Exp]) -> None:
        jmp_pc = self.PC + 1
        self.emit(Opcode.JMP_imm, [], [None])

        fn_atom, args_exp, body_exprs = operands
        fn_name = fn_atom.value.value
        args = [a.value.value for a in args_exp.operands]

        self.var_allocator.push_fn_scope(fn_name, args)
        args_slots = [self.var_allocator[p] for p in args]

        self.label_map[fn_name] = {
            "address": Address(self.PC),
            "args_amount": len(args),
            "locals_amount": None,
        }

        tmp_ret = self.reg_controller.alloc()
        self.emit(Opcode.POP, [Term(tmp_ret)], [])

        for slot in args_slots:
            tmp = self.reg_controller.alloc()
            self.emit(Opcode.POP, [Term(tmp)], [])
            self.emit(Opcode.STORE_r2da, [Term(tmp)], [slot.value])
            self.reg_controller.release(tmp)

        self.emit(Opcode.PUSH, [Term(tmp_ret)], [])
        self.reg_controller.release(tmp_ret)

        [self.generate(exp) for exp in body_exprs.operands[:-1]]
        ret_reg = self.generate(body_exprs.operands[-1])


        if isinstance(ret_reg, Address):
            self.emit(Opcode.MOV_da2r, [Term(Registers.Registers.R0)], [ret_reg.value])
        elif isinstance(ret_reg, Registers.Registers):
            self.emit(Opcode.MOV_r2r, [Term(Registers.Registers.R0), Term(ret_reg)], [])
            self.reg_controller.release(ret_reg)
        else:
            err_message = f"incorrect operand type: {ret_reg}"
            raise TypeError(err_message)

        self.emit(Opcode.RET, [], [])

        self.var_allocator.pop_fn_scope()

        self.program[jmp_pc] = self.PC


    def handle_call(self, op: Operation, operands: list[Exp | Atom]) -> Registers.Registers:
        fn_name = op.value.value

        for param in self.var_allocator.scopes[-1]:
            temp = self.reg_controller.alloc()
            self.emit(Opcode.MOV_da2r, [Term(temp)], [self.var_allocator[param].value])
            self.emit(Opcode.PUSH, [Term(temp)], [])
            self.reg_controller.release(temp)

        for arg_expr in reversed(operands):
            value = self.generate(arg_expr)

            if isinstance(value, Registers.Registers):
                self.emit(Opcode.PUSH, [Term(value)], [])
                self.reg_controller.release(value)
            else:
                tmp = self.reg_controller.alloc()
                self.emit(Opcode.MOV_da2r, [Term(tmp)], [value.value])
                self.emit(Opcode.PUSH, [Term(tmp)], [])
                self.reg_controller.release(tmp)

        self.emit(Opcode.CALL, [], [self.label_map[fn_name]["address"].value])

        for param in reversed(self.var_allocator.scopes[-1]):
            param_reg = self.reg_controller.alloc()
            self.emit(Opcode.POP, [Term(param_reg)], [])
            self.emit(Opcode.STORE_r2da, [Term(param_reg)],[self.var_allocator[param].value])
            self.reg_controller.release(param_reg)

        return Registers.Registers.R0

MAX_REGISTER = 7
MIN_REGISTER = 1
class RegisterController:
    def __init__(self):
        self.available = [1, 2, 3, 4, 5, 6, 7]

    def alloc(self) -> Registers.Registers:
        return Registers.Registers(self.available.pop())

    def release(self, reg: Registers.Registers) -> None:
        if MIN_REGISTER <= reg.value <= MAX_REGISTER:
            self.available.append(reg.value)


class VariableAllocator:
    def __init__(self, base_address: int = 900) -> None:
        self.next_free = base_address
        self.scopes: list[dict[str, Address]] = [{}]

    def _new_addr(self) -> Address:
        addr = Address(self.next_free)
        self.next_free += 1
        return addr

    def get(self, name: str) -> Address:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise KeyError(name)

    def allocate(self, name: str) -> Address:
        scope = self.scopes[-1]
        if name not in scope:
            scope[name] = self._new_addr()
        return scope[name]

    def push_fn_scope(self, fn_name: str, params: list[str]) -> None:
        frame: dict[str, Address] = {}
        for p in params:
            if p in frame:
                err_message = f"parameter {p!r} repeated"
                raise SyntaxError(err_message)
            frame[p] = self._new_addr()
        self.scopes.append(frame)

    def pop_fn_scope(self) -> None:
        if len(self.scopes) == 1:
            err_message = "pop on global scope"
            raise RuntimeError(err_message)
        self.scopes.pop()

    def __getitem__(self, name: str) -> Address:
        return self.get(name)


def to_bytes(code):
    """Преобразует инструкции в бинарное представление"""
    binary_bytes = bytearray()
    for instr in code:
        if isinstance(instr, Instruction):
            # Получаем бинарный код операции
            binary_instr = instr.opcode.value << 22
            for i, term in enumerate(instr.terms):
                binary_instr = binary_instr | (term.value.value << (19 - i * 3))
            # Преобразуем 32-битное целое число в 4 байта (big-endian)
            binary_bytes.extend(
                ((binary_instr >> 24) & 0xFF, (binary_instr >> 16) & 0xFF, (binary_instr >> 8) & 0xFF, binary_instr & 0xFF)
            )
        else:
            binary_bytes.extend(
                ((instr >> 24) & 0xFF, (instr >> 16) & 0xFF, (instr >> 8) & 0xFF, instr & 0xFF)
            )            

    return bytes(binary_bytes)


def main(source, target):
    """Функция запуска транслятора. Параметры -- исходный и целевой файлы."""
    reg_controller = RegisterController()
    var_allocator = VariableAllocator()
    program = [0] * 1024

    tokenizer = Tokenizer()
    parser = Parser()
    generator = Generator(var_allocator, reg_controller, program)

    with open(source, encoding="utf-8") as f:
        source = f.read()

    generator.generate(parser.parse(tokenizer.tokenize(source)))

    with open(target, 'wb') as f:
        f.write(to_bytes(program[:generator.PC]))

if __name__ == '__main__':
    main('src/file.lisp', 'out.bin')

    # with open('out.bin', 'rb') as f:
    #     bin_code = f.read()

    # print(from_bytes(bin_code))

# # TODO fix scopes parser: if (( or )) work incorrect
# if __name__ == "__main__":
#     reg_controller = RegisterController()
#     var_allocator = VariableAllocator()
    

#     # expression = """
#     # (begin
#     #     (defun square (begin x) (begin (* x x)))
#     #     (setq a (square 12))
#     # )
#     # """
#     expression = """
#     (begin
#         (setq a 3)
#         (defun square (begin x) (begin (* x x)))
#         (defun factorial (begin x)
#             (begin
#                 (setq b (square x))
#                 (cond
#                     (<= x 1) (begin 1)
#                     (> x 1) (begin (* x (factorial (- x 1))))
#                 )
#             )
#         )
#         (setq a (factorial a))
#     )
#     """
#     # expression = """
#     #     (begin
#     #         (setq a (cond (> 5 3) (begin (setq i 1))
#     #                       (> 1 3) (begin (setq j 1))
#     #         ))
#     #     )
#     # """
#     # expression = """(+ 1 (* 2 3))"""
#     # expression = """
#     # (begin
#     #     (setq i 0)
#     #     (setq n 10)
#     #     (setq sum 0)
#     #     (setq sum2 0)
#     #     (while (<= i n)
#     #         (setq sum (+ sum i))
#     #         (setq sum2 (+ sum2 (* i i)))
#     #         (setq i (+ i 1))
#     #     )
#     #     (setq sum (* sum sum))
#     #     (setq res (- sum sum2))
#     # )
#     # """
#     #     expression = """
#     # (begin
#     #     (setq n 10)
#     #     (setq sum 0)
#     #     (setq sum2 0)
#     #     (setq i 0)
#     #     (while (< i n)
#     #         (setq sum (+ sum i))
#     #         (setq sum2 (+ sum2 (* i i)))
#     #         (setq i (+ i 1))
#     #     )
#     #     (setq num (+ 1 2))
#     # )
#     #     """
#     dp = DataPath(input_address=0, output_address=0)

#     memory = dp.memory
#     program = Program(memory)

#     tokenizer = Tokenizer()
#     parser = Parser()
#     generator = Generator(var_allocator, reg_controller, program)
#     print(
#         generator.generate(
#             parser.parse(tokenizer.tokenize(expression)),
#         ),
#     )   
#     print(memory[Address(2)])
#     print(to_bytes([memory[Address(2)]]))
#     # inv_var_map = {v.value: k for k, v in var_allocator.var_map.items()}
#     inv_var_map: dict[int, str] = {}
#     for i in range(generator.PC + 2):
#         if isinstance(memory[Address(i)], Instruction):
#             print(f"{i}: {memory[Address(i)]}")
#         elif memory[Address(i)] in inv_var_map:
#             print(f"{i}({inv_var_map[memory[Address(i)]]}): {memory[Address(i)]}")
#         else:
#             print(f"{i}: {memory[Address(i)]}")

#     dp.program_counter = 0
#     MAX_CYCLES = 1_000_000
#     for cycle in range(MAX_CYCLES):
#         dp.control_unit.run_single_micro()
#         print(dp)
#         if dp.program_counter >= generator.PC:
#             print(f"\nProgram finished after {cycle + 1} micro-cycles.")
#             break
#     else:
#         print("cycle limit hit")

#     print("\nRegister file:")
#     for r, v in dp.registers.registers_value.items():
#         print(f"  {r.name:3} = {v}")

#     print()
#     # inv_var_map = {v.value: k for k, v in var_allocator.var_map.items()}
#     inv_var_map = {}
#     for i in range(900, 910):
#         if isinstance(memory[Address(i)], Instruction):
#             print(f"{i}: {memory[Address(i)]}")
#         elif memory[Address(i)] in inv_var_map:
#             print(f"{i}({inv_var_map[memory[Address(i)]]}): {memory[Address(i)]}")
#         else:
#             print(f"{i}: {memory[Address(i)]}")
#     print("\n")
