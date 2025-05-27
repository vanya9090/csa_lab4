from enum import Enum
from dataclasses import dataclass
from typing import Union, Callable
from isa import Instruction, Opcode, Term
from machine.machine import Registers

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

@dataclass
class Exp:
    operation : Union[Operation, Atom]
    operands : list[Union[Atom, 'Exp']]


BINOP_OPCODE : dict[Operation, Opcode] = {
    Operation.ADD : Opcode.ADD_mem,
    Operation.SUB : Opcode.SUB_mem,
    Operation.MUL : Opcode.MUL_mem,
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

# генерация asm кода из AST
class Generator:
    def __init__(self, var_allocator : "VariableAllocator", reg_controller : "RegisterController"):
        self.handlers_map : dict[str, Callable[[list], None]] = {
            'begin': self.handle_token_begin,
            'setq': self.handle_token_setq,
            'binop': self.handle_token_binop,
        }
        self.var_allocator = var_allocator
        self.reg_controller = reg_controller

    def generate(self, expression : Union[Exp, Atom]):
        if isinstance(expression, Atom):
            # print("Atom:", expression.value)
            return self.handle_atom(expression)
        elif isinstance(expression, Exp):
            op = expression.operation
            if isinstance(op, Operation):
                # print("Operation:", op)
                return self.handlers_map['binop'](op, expression.operands)
            elif isinstance(op, Atom):
                if isinstance(op.value, Symbol):
                    if op.value.value in self.handlers_map:
                        # print("Operation:", op)
                        return self.handlers_map[op.value.value](expression.operands)
                    else:
                        raise NotImplementedError(f"function {op.value.value} not handled")
                else:
                    raise RuntimeError(f"operation: f{op}")
                
    def handle_atom(self, atom : Atom) -> Union[Registers.Registers, int]:
        if isinstance(atom.value, Number):
            return atom.value.value
        elif isinstance(atom.value, Symbol):
            return self.var_allocator.allocate(atom.value.value)
        else:
            raise RuntimeError(f"{atom} isn't Atom")

    def handle_token_binop(self, operation : Operation, operands : list[Exp]):
        first = self.generate(operands[0])
        second = self.generate(operands[1])

        dst_reg = self.reg_controller.alloc()
        print(Instruction(BINOP_OPCODE[operation], [dst_reg, first, second]))
        return dst_reg
    

    def handle_token_begin(self, operands : list[Exp]):
        [self.generate(operand) for operand in operands]

    def handle_token_setq(self, operands : list[Exp]):
        var_reg = self.generate(operands[0])
        varvalue = self.generate(operands[1])
        
        print(Instruction(Opcode.MOV_imm2r, [var_reg, varvalue]))

        return var_reg


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
    def __init__(self, reg_controller):
        self.var_map : dict[str, Registers.Registers] = {}
        self.reg_controller = reg_controller

    def allocate(self, varname : str) -> Registers.Registers:
        if varname in self.var_map:
            return self.var_map[varname]
        reg = self.reg_controller.alloc()
        self.var_map[varname] = reg
        return reg
    
    def __getitem__(self, varname : str):
        return self.var_map[varname]


if __name__ == "__main__":
    reg_controller = RegisterController()
    var_allocator = VariableAllocator(reg_controller)

    # expression = """(+ 1 (* 2 3))"""
    expression = """(begin (setq r 8) (* 3 (* r r)))"""
    tokenizer = Tokenizer()
    parser = Parser()
    generator = Generator(var_allocator, reg_controller)
    print(tokenizer.tokenize(expression))
    print(parser.parse(tokenizer.tokenize(expression)))
    print()
    print(generator.generate(parser.parse(tokenizer.tokenize(expression))))


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