from enum import Enum
from dataclasses import dataclass
from typing import Union, Callable
from isa import Instruction, Opcode, Term
from machine.machine import Registers, Memory, Address

@dataclass
class Number:
    value : int

@dataclass
class Symbol:
    value : str

@dataclass
class Atom:
    value : Union[Number, Symbol]

class Operation(Enum):
    ADD = '+'
    SUB = '-' 
    MUL = '*'
    DIV = '/'
    RMD = '%'
    LT = '<'
    GT = '>'
    EQ = '='

@dataclass
class Exp:
    operation : Union[Operation, Atom]
    operands : list[Union[Atom, 'Exp']]


BINOP_OPCODE : dict[Operation, Opcode] = {
    Operation.ADD: Opcode.ADD_mem,
    Operation.SUB: Opcode.SUB_mem,
    Operation.MUL: Opcode.MUL_mem,
    Operation.LT: Opcode.LT,
    Operation.GT: Opcode.GT,
    Operation.EQ: Opcode.EQ,
}


# первоначальный этап обработки программы на LISP 
class Tokenizer:
    def tokenize(self, s : str) -> list[str]:
        return s.replace('(',' ( ').replace(')',' ) ').split()

# создание AST
class Parser:
    def parse(self, tokens: list[str]) -> Union[Exp, Atom]:
        if not tokens:
            raise SyntaxError('unexpected EOF')

        token = tokens.pop(0)

        if token == '(':
            if not tokens:
                raise SyntaxError('missing operation after "("')
            op_token = tokens.pop(0)
            try:
                op = Operation(op_token)
            except ValueError:
                op = self.atom(op_token) # created functions
            
            args = []
            while tokens[0] != ')':
                args.append(self.parse(tokens))
            tokens.pop(0)  # remove ')'
            return Exp(operation=op, operands=args)

        elif token == ')':
            raise SyntaxError("unexpected ')'")
        else:
            return self.atom(token)

    def atom(self, token: str) -> Atom:
        try:
            return Atom(Number(int(token)))
        except ValueError:
            return Atom(Symbol(token))
        
class Program:
    def __init__(self, memory : Memory):
        self.memory = memory
        self.idx = 0

# генерация asm кода из AST
class Generator:
    def __init__(self, var_allocator : "VariableAllocator", reg_controller : "RegisterController", program : Program):
        self.handlers_map : dict[str, Callable[[list], None]] = {
            'begin': self.handle_token_begin,
            'setq': self.handle_token_setq,
            'binop': self.handle_token_binop,
            'defun': None,
            'while': self.handle_while,

        }
        self.var_allocator = var_allocator
        self.reg_controller = reg_controller
        self.program = program
        self.PC = 0

    def generate(self, expression : Union[Exp, Atom], dst_type : Union[Address, Registers.Registers, Number, None]):
        if isinstance(expression, Atom):
            return self.handle_atom(expression)
        elif isinstance(expression, Exp):
            op = expression.operation
            if isinstance(op, Operation):
                return self.handlers_map['binop'](op, expression.operands, dst_type)
            elif isinstance(op, Atom):
                if isinstance(op.value, Symbol):
                    if op.value.value in self.handlers_map:
                        return self.handlers_map[op.value.value](expression.operands, dst_type)
                    else:
                        raise NotImplementedError(f"function {op.value.value} not handled")
                else:
                    raise RuntimeError(f"operation: f{op}")

    def handle_atom(self, atom : Atom) -> Union[Address, Number]:
        if isinstance(atom.value, Symbol):
            address = self.var_allocator.allocate(atom.value.value)
            return address
        return atom.value

    # def handle_atom(self, atom : Atom) -> Address:
    #     if isinstance(atom.value, Symbol):
    #         address = self.var_allocator.allocate(atom.value.value)
    #         return address
    #     elif isinstance(atom.value, Number):
    #         self.PC += 1
    #         return Address(self.PC)
    #     else:
    #         raise RuntimeError(f"{atom} isn't atom")

    def handle_token_binop(self, operation : Operation, operands : list[Exp], dst_type : Union[Address, Registers.Registers]) -> Union[Address, Registers.Registers]:
        first : Union[Address, Number] = self.generate(operands[0], dst_type=Address)
        second : Union[Address, Number] = self.generate(operands[1], dst_type=Address)

        if isinstance(first, Number):
            first : Address = self.PC
        if isinstance(second, Number):
            second : Address = self.PC

        reg = self.reg_controller.alloc()
        print(self.PC, [Instruction(BINOP_OPCODE[operation], [reg]), first, second])
        self.PC += 3

        if dst_type == Registers.Registers:
            return reg
        elif dst_type == Address:
            temp_add = self.var_allocator.allocate('temp')
            print(self.PC, [Instruction(Opcode.STORE_r2da, [reg]), temp_add])
            self.PC += 2
            return temp_add 
        else:
            raise RuntimeError(f"{dst_type} isn't dst type")

    def handle_token_begin(self, operands : list[Exp], dst_type : None) -> None:
        [self.generate(operand, dst_type=Address) for operand in operands]

    def handle_token_setq(self, operands : list[Exp], dst_type : Address) -> Address:
        var_address : Address = self.generate(operands[0], dst_type=Address)
        var_value : Union[Number, Registers.Registers] = self.generate(operands[1], dst_type=Registers.Registers)
        if isinstance(var_value, Number):
            self.program.memory[var_address] = var_value.value
        elif isinstance(var_value, Registers.Registers):
            print(self.PC, [Instruction(Opcode.STORE_r2da, [var_value]), var_address])
            self.PC += 2
            self.reg_controller.release(var_value)
        else:
            raise RuntimeError(f"{var_value} isn't dst type")

        return var_value

    def handle_while(self, operands : list[Exp], dst_type : Address) -> None:
        start_PC = self.PC
        condition_res_reg : Registers.Registers = self.generate(operands[0], dst_type=Registers.Registers)
        print(self.PC, [Instruction(Opcode.BEQZ, [condition_res_reg]), [None]])
        self.PC += 2
        [self.generate(operand, dst_type=Address) for operand in operands[1:]]
        print(self.PC, [Instruction(Opcode.JMP_imm, []), start_PC])
        self.PC += 2
        self.reg_controller.release(condition_res_reg)



# класс, который отвечает за обработку и хранение лейблов (label -> address map)
class LabelController:
    pass

# RegisterController - хранить в себе стек свободных регистров регистров, аллоцирует регистры и освобождает их
# в регистрах могут лежать переменные (TODO частоиспользуемые) и какие-то промежуточные значения
class RegisterController:
    def __init__(self):
        self.available = [3,4,5,6,7,8,9,10]
    def alloc(self):
        return Registers.Registers(self.available.pop())
    def release(self, reg):
        self.available.append(reg)

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
    
    def __setitem__(self, varname: str, address: int):
        self.var_map[varname] = address


if __name__ == "__main__":
    reg_controller = RegisterController()
    var_allocator = VariableAllocator()

    # expression = """(+ 1 (* 2 3))"""
    # expression = """(begin (setq r 8) (* 3 (* r r)))"""
    expression = """
(begin
    (setq n 10)
    (setq sum 0)
    (setq sum2 0)
    (setq i 0)
    (while (< i n)
        (setq sum (+ sum i))
        (setq sum2 (+ sum2 (* i i)))
        (setq i (+ i 1))
    ) 
    (setq num (+ 1 2))
)
    """
    memory = Memory(1024)
    program = Program(memory)

    tokenizer = Tokenizer()
    parser = Parser()
    generator = Generator(var_allocator, reg_controller, program)
    print(tokenizer.tokenize(expression))
    print(parser.parse(tokenizer.tokenize(expression)))
    print()
    print(generator.generate(parser.parse(tokenizer.tokenize(expression)), dst_type=Address))
    print()
    print(' '.join(str(memory[Address(i)]) for i in range(0, 10)))
    print(var_allocator.var_map)

# доступ к immeadiate есть напрямую, потому что они хранятся отдельным словом в памяти и мы знаем их адрес

#TODO 
# на данный момент все переменные хранятся в регистрах
# минусы: ограниченное количество
# плюсы: быстрый доступ

# можно сохранять все переменные в память
# минусы: долгий доступ, а что тогда вообще хранить в регистрах???
# плюсы: неограниченное количество, (уже есть реализованные команды ADD, MUL, SUB, ... )
# вероятно, immediate значения придется тоже складывать в память в к коммандах ADD, MUL, ...

# хранить переменные и там и там
# минусы: сложная реализация
# плюсы: хайпово звучит