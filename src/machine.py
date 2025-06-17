import logging
import sys
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

from enums import ALUOperations, Sel, Signal
from isa import OPCODE_TO_TERMS_AMOUNT, Instruction, Opcode, Term
from microprogram import mprogram

MAX_CYCLES = 20_000

class HltError(Exception):
    pass

N_ALU_mem_operations = (
    Opcode.NADD_mem,
    Opcode.NSUB_mem,
    Opcode.NMUL_mem,
    Opcode.NAND_mem,
    Opcode.NOR_mem,
)
ALU_reg2reg_operations = (
    Opcode.ADD_reg2reg,
    Opcode.SUB_reg2reg,
    Opcode.MUL_reg2reg,
    Opcode.DIV_reg2reg,
    Opcode.AND_reg2reg,
    Opcode.OR_reg2reg,
    Opcode.XOR_reg2reg,
    Opcode.RMD_reg2reg,
)
ALU_mem2reg_operations = (
    Opcode.ADD_mem2reg,
    Opcode.SUB_mem2reg,
    Opcode.MUL_mem2reg,
    Opcode.DIV_mem2reg,
    Opcode.AND_mem2reg,
    Opcode.OR_mem2reg,
    Opcode.XOR_mem2reg,
    Opcode.RMD_mem2reg,
)
ALU_mix2reg1_operations = (
    Opcode.ADD_mix2reg1,
    Opcode.SUB_mix2reg1,
    Opcode.MUL_mix2reg1,
    Opcode.DIV_mix2reg1,
    Opcode.AND_mix2reg1,
    Opcode.OR_mix2reg1,
    Opcode.XOR_mix2reg1,
    Opcode.RMD_mix2reg1,
)
ALU_mix2reg2_operations = (
    Opcode.ADD_mix2reg1,
    Opcode.SUB_mix2reg2,
    Opcode.MUL_mix2reg1,
    Opcode.DIV_mix2reg2,
    Opcode.AND_mix2reg1,
    Opcode.OR_mix2reg1,
    Opcode.XOR_mix2reg1,
    Opcode.RMD_mix2reg2,
)
ALU_mem2mem_operations = (
    Opcode.ADD_mem2mem,
    Opcode.SUB_mem2mem,
    Opcode.MUL_mem2mem,
    Opcode.DIV_mem2mem,
    Opcode.AND_mem2mem,
    Opcode.OR_mem2mem,
    Opcode.XOR_mem2mem,
    Opcode.RMD_mem2mem,
)

MOV_codes = (
    Opcode.MOV_r2r,
    Opcode.MOV_rd2r,
    Opcode.MOV_imm2r,
    Opcode.MOV_da2r,
    Opcode.MOV_ia2r,
    Opcode.MOV_mem2mem,
    Opcode.MOV_ri2r,
)
INC_DEC_codes = (Opcode.INC_mem, Opcode.INC_r, Opcode.DEC_mem, Opcode.DEC_r)
STORE_codes = (
    Opcode.STORE_r2rd,
    Opcode.STORE_r2ri,
    Opcode.STORE_r2ia,
    Opcode.STORE_r2da,
)


class ALU:
    class Flags(Enum):
        ZERO: int = 0
        CARRY: int = 1
        OVERFLOW: int = 2
        NEGATIVE: int = 3

    def __init__(self, datapath: "DataPath"):
        self.datapath = datapath

        self.__left_term: int = 0
        self.__right_term: int = 0
        self.result: int = 0
        self.flags: dict[ALU.Flags, bool] = {
            self.Flags.ZERO: False,
            self.Flags.CARRY: False,
            self.Flags.OVERFLOW: False,
            self.Flags.NEGATIVE: False,
        }
        self.__operations: dict[ALUOperations, Callable[[int, int], int]] = {
            ALUOperations.ADD: lambda x, y: x + y,
            ALUOperations.SUB: lambda x, y: x - y,
            ALUOperations.AND: lambda x, y: x & y,
            ALUOperations.OR: lambda x, y: x | y,
            ALUOperations.XOR: lambda x, y: x ^ y,
            ALUOperations.MUL: lambda x, y: x * y,
            ALUOperations.DIV: lambda x, y: x // y,
            ALUOperations.RMD: lambda x, y: x % y,
        }

    def __set_flags(self) -> None:
        self.flags[self.Flags.ZERO] = self.result == 0
        self.flags[self.Flags.NEGATIVE] = self.result < 0
        self.flags[self.Flags.CARRY] = self.result > (2**31 - 1)

    # left alu only can get src_left_register
    def latch_left_alu(self, sel: Sel.LeftALU) -> None:
        assert isinstance(sel, Sel.LeftALU), "selector must be LeftALU selector"

        if sel == Sel.LeftALU.REGISTER:
            self.__left_term = self.datapath.registers[self.datapath.src_left_register]
        if sel == Sel.LeftALU.ZERO:
            self.__left_term = 0
        if sel == Sel.LeftALU.PLUS_1:
            self.__left_term = 1
        if sel == Sel.LeftALU.MINUS_1:
            self.__left_term = -1
        if sel == Sel.LeftALU.PC:
            self.__left_term = self.datapath.program_counter
        if sel == Sel.LeftALU.DR:
            self.__left_term = self.datapath.data_register

    # right alu only can get src_right_register
    def latch_right_alu(self, sel: Sel.RightALU) -> None:
        assert isinstance(sel, Sel.RightALU), "selector must be RightALU selector"

        if sel == Sel.RightALU.REGISTER:
            self.__right_term = self.datapath.registers[
                self.datapath.src_right_register
            ]
        if sel == Sel.RightALU.DR:
            self.__right_term = self.datapath.data_register
        if sel == Sel.RightALU.PLUS_1:
            self.__right_term = 1
        if sel == Sel.RightALU.PLUS_2:
            self.__right_term = 2
        if sel == Sel.RightALU.MINUS_1:
            self.__right_term = -1
        if sel == Sel.RightALU.ZERO:
            self.__right_term = 0

    def perform(self, operation: ALUOperations) -> None:
        self.result = self.__operations[operation](self.__left_term, self.__right_term)
        self.__set_flags()


class Registers:
    class Registers(Enum):
        R0: int = 0
        R1: int = 1
        R2: int = 2
        R3: int = 3
        R4: int = 4
        R5: int = 5
        RSP: int = 6
        RHP: int = 7

    def __init__(self) -> None:
        self.registers_value: dict[Registers.Registers, int] = {
            Registers.Registers.RSP: 0,
            Registers.Registers.RHP: 0,
            Registers.Registers.R0: 0,
            Registers.Registers.R1: 0,
            Registers.Registers.R2: 0,
            Registers.Registers.R3: 0,
            Registers.Registers.R4: 0,
            Registers.Registers.R5: 0,
        }

    def __getitem__(self, key: Registers) -> int:
        return self.registers_value[key]

    def __setitem__(self, key: Registers, value: int) -> None:
        self.registers_value[key] = value

    def latch_rsp(self, sel: Sel.RSP) -> None:
        if sel == Sel.RSP.PLUS_1:
            self.registers_value[Registers.Registers.RSP] += 1
        if sel == Sel.RSP.MINUS_1:
            self.registers_value[Registers.Registers.RSP] -= 1


@dataclass
class Address:
    value: int


class Memory:
    def __init__(self, memory_size: int):
        self.memory_size = memory_size
        self.memory: list[int | Instruction | None] = [0] * memory_size

    def __getitem__(self, key: Address) -> int | Instruction | None:
        return self.memory[key.value]

    def __setitem__(self, key: Address, value: int | Instruction | None) -> None:
        self.memory[key.value] = value


class ControlUnit:
    def __init__(self, datapath: "DataPath"):
        self.datapath = datapath

        self.mprogram_counter: int = 0

        self.mem_address: int = 0
        self.n: int = 0

        self.signals: dict[Signal, Callable[..., None]] = {
            Signal.LATCH_N: self.latch_n,
            Signal.LATCH_INSTRUCTION: self.latch_instruction,
            Signal.LATCH_PROGRAM_COUNTER: self.datapath.latch_program_counter,
            Signal.LATCH_JUMP: self.datapath.latch_jump,
            Signal.LATCH_FLAG: self.datapath.latch_flag,
            Signal.LATCH_INVERSE: self.datapath.latch_inverse,
            Signal.LATCH_MPROGRAM_COUNTER: self.latch_mprogram_counter,
            Signal.LATCH_ADDRESS_REGISTER: self.datapath.latch_address_register,
            Signal.LATCH_DATA_REGISTER: self.datapath.latch_data_register,
            Signal.LATCH_LEFT_ALU: self.datapath.alu.latch_left_alu,
            Signal.LATCH_RIGHT_ALU: self.datapath.alu.latch_right_alu,
            Signal.EXECUTE_ALU: self.datapath.alu.perform,
            Signal.LATCH_REGISTER: self.datapath.latch_register,
            Signal.LATCH_MEMORY: self.datapath.latch_memory,
            Signal.LATCH_RSP: self.datapath.registers.latch_rsp,
            Signal.HLT: self.datapath.hlt,
        }

        self.mprogram = mprogram

    def decode(self, instruction: Instruction) -> None:
        self.opcode: Opcode = instruction.opcode
        self.terms: list[Term] = instruction.terms
        if self.opcode in MOV_codes:
            if self.opcode in (Opcode.MOV_r2r, Opcode.MOV_rd2r, Opcode.MOV_ri2r):
                self.datapath.select_dst_register(self.terms[0].value)
                self.datapath.select_left_register(self.terms[1].value)
            elif self.opcode == Opcode.MOV_mem2mem:
                pass
            else:
                self.datapath.select_dst_register(self.terms[0].value)

        elif self.opcode in INC_DEC_codes:
            if self.opcode in (Opcode.INC_r, Opcode.DEC_r):
                self.datapath.select_dst_register(self.terms[0].value)
                self.datapath.select_left_register(self.terms[0].value)

        elif self.opcode in STORE_codes:
            if self.opcode in (Opcode.STORE_r2rd, Opcode.STORE_r2ri):
                self.datapath.select_right_register(self.terms[0].value)
                self.datapath.select_left_register(self.terms[1].value)
            else:
                self.datapath.select_right_register(self.terms[0].value)

        elif self.opcode in N_ALU_mem_operations:
            self.n = self.terms[0].value
            self.datapath.select_dst_register(self.terms[1].value)
            self.datapath.select_left_register(self.terms[1].value)

        elif self.opcode in (
            Opcode.BEQZ,
            Opcode.BNEZ,
            Opcode.BGZ,
            Opcode.BLZ,
        ) or self.opcode in (Opcode.PUSH, Opcode.JMP_r):
            self.datapath.select_left_register(self.terms[0].value)
        elif self.opcode in (Opcode.JMP_imm, Opcode.CALL, Opcode.RET):
            pass

        elif self.opcode in ALU_reg2reg_operations:
            self.datapath.select_dst_register(self.terms[0].value)
            self.datapath.select_left_register(self.terms[1].value)
            self.datapath.select_right_register(self.terms[2].value)
        elif self.opcode in ALU_mem2reg_operations:
            self.datapath.select_dst_register(self.terms[0].value)
        elif self.opcode in ALU_mix2reg1_operations:
            self.datapath.select_dst_register(self.terms[0].value)
            self.datapath.select_left_register(self.terms[1].value)  # set left register
        elif self.opcode in ALU_mix2reg2_operations:
            self.datapath.select_dst_register(self.terms[0].value)
            self.datapath.select_right_register(self.terms[1].value)  # set right register
        elif self.opcode in ALU_mem2mem_operations:
            pass

        elif self.opcode == Opcode.PUSH:
            self.datapath.select_left_register(self.terms[0].value)
        elif self.opcode == Opcode.POP:
            self.datapath.select_dst_register(self.terms[0].value)
        elif self.opcode == Opcode.HLT:
            pass
        elif self.opcode == Opcode.GET_CARRY:
            self.datapath.select_dst_register(self.terms[0].value)
        else:
            raise RuntimeError

    def latch_mprogram_counter(self, sel: Sel.MProgramCounter) -> None:
        assert isinstance(sel, Sel.MProgramCounter), (
            "selector must be MProgramCounter selector"
        )

        if sel == Sel.MProgramCounter.ZERO:
            self.mprogram_counter = 0
        if sel == Sel.MProgramCounter.PLUS_1:
            self.mprogram_counter += 1
        if sel == Sel.MProgramCounter.OPCODE:
            self.mprogram_counter = self.opcode.value
        if sel == Sel.MProgramCounter.N:
            if self.n == 0:
                self.mprogram_counter += 1
            else:
                self.mprogram_counter = self.opcode.value

    def latch_instruction(self) -> None:
        assert isinstance(self.datapath.data_register, Instruction)
        self.decode(self.datapath.data_register)

    def latch_n(self, sel: Sel.N) -> None:
        assert isinstance(sel, Sel.N), "selector must be N selector"

        if sel == Sel.N.DECODER:
            self.n = self.terms[0].value
        if sel == Sel.N.MINUS_1:
            self.n -= 1
        if sel == Sel.N.ZERO:
            self.n = 0

    def execute_signal(self, signal: Signal, *arg: tuple[Signal, None | Sel]) -> None:
        self.signals[signal](*arg)

    def run_single_micro(self) -> None:
        mpc_now = self.mprogram_counter
        signal, *maybe_sel = self.mprogram[mpc_now]
        if maybe_sel and maybe_sel[0] is not None:
            self.execute_signal(signal, maybe_sel[0])
        else:
            self.execute_signal(signal)
        self.datapath.tick += 1
        if self.mprogram_counter == mpc_now:
            self.mprogram_counter += 1


class DataPath:
    def __init__(self, input_address: int, output_address: int):
        self.tick = 0
        self.alu: ALU = ALU(self)
        self.registers: Registers = Registers()
        self.control_unit: ControlUnit = ControlUnit(self)
        self.memory = Memory(1024)
        self.registers[Registers.Registers.RSP] = 1023
        self.registers[Registers.Registers.RHP] = 500

        self.program_counter: int = 0
        self.selected_flag: ALU.Flags | None = None
        self.inverse_flag: bool = False
        self.jump_register: int = 0

        self.data_register: int = 0
        self.address_register: int = 0

        self.src_left_register: Registers.Registers = Registers.Registers.R5
        self.src_right_register: Registers.Registers = Registers.Registers.R4
        self.dst_register: Registers.Registers = Registers.Registers.R3

        self.input_address: int = input_address
        self.output_address: int = output_address

        self.input_buffer: list[str] = []
        self.output_buffer: list[str] = []

    def select_left_register(self, register: Registers.Registers) -> None:
        self.src_left_register = register

    def select_right_register(self, register: Registers.Registers) -> None:
        self.src_right_register = register

    def select_dst_register(self, register: Registers.Registers) -> None:
        self.dst_register = register

    def latch_jump(self, sel : Sel.Jump) -> None:
        self.jump_register = self.alu.result

    def latch_flag(self, sel: Sel.Flag) -> None:
        if sel == Sel.Flag.CARRY:
            self.selected_flag = ALU.Flags.CARRY
        if sel == Sel.Flag.OVERFLOW:
            self.selected_flag = ALU.Flags.OVERFLOW
        if sel == Sel.Flag.NEGATIVE:
            self.selected_flag = ALU.Flags.NEGATIVE
        if sel == Sel.Flag.ZERO:
            self.selected_flag = ALU.Flags.ZERO
        if sel == Sel.Flag.NONE:
            self.selected_flag = None

    def latch_inverse(self, sel: Sel.Inverse) -> None:
        if sel == Sel.Inverse.IDENTITY:
            self.inverse_flag = False
        if sel == Sel.Inverse.INVERSE:
            self.inverse_flag = True

    def latch_program_counter(self, sel: Sel.ProgramCounter) -> None:
        assert isinstance(sel, Sel.ProgramCounter), (
            "selector must be ProgramCounter selector"
        )
        if sel == Sel.ProgramCounter.CONDITION:
            if self.selected_flag is None or self.alu.flags[self.selected_flag] ^ self.inverse_flag:
                self.program_counter = self.jump_register
            else:
                self.program_counter += 1
        if sel == Sel.ProgramCounter.NEXT:
            self.program_counter += 1

    def latch_data_register(self, sel: Sel.DataRegister) -> None:
        assert isinstance(sel, Sel.DataRegister)

        if sel == Sel.DataRegister.ALU:
            self.data_register = self.alu.result
        elif sel == Sel.DataRegister.MEMORY:
            if 0 > self.address_register > self.memory.memory_size:
                raise ValueError("Memory cell number out of bounds")
            if self.address_register == self.output_address:
                raise ValueError("Can't read from output port")
            if self.address_register == self.input_address:
                try:
                    self.data_register = self.input_buffer.pop(0)
                except IndexError:
                    raise HltError
            else:
                self.data_register = self.memory[Address(self.address_register)]

    def latch_address_register(self, sel: Sel.AddressRegister) -> None:
        assert isinstance(sel, Sel.AddressRegister), (
            "selector must be AddressRegister selector"
        )

        if sel == Sel.AddressRegister.CONTROL_UNIT:
            self.address_register = self.program_counter
        elif sel == Sel.AddressRegister.ALU:
            self.address_register = self.alu.result
        elif sel == Sel.AddressRegister.RSP:
            self.address_register = self.registers[Registers.Registers.RSP]
        elif sel == Sel.AddressRegister.DR:
            self.address_register = self.data_register

    def latch_register(self, sel: Sel.Register) -> None:
        assert isinstance(sel, Sel.Register), "selector must be Register selector"

        if sel == Sel.Register.ALU:
            self.registers[self.dst_register] = self.alu.result
        elif sel == Sel.Register.DR:
            self.registers[self.dst_register] = self.data_register
        elif sel == Sel.Register.REGISTER:
            self.registers[self.dst_register] = self.registers[self.src_left_register]
        elif sel == Sel.Register.CARRY:
            self.registers[self.dst_register] = self.alu.flags[self.alu.Flags.CARRY]

    def latch_memory(self) -> None:
        if 0 > self.address_register > self.memory.memory_size:
            raise ValueError("Memory cell number out of bounds")
        if self.address_register == self.input_address:
            raise ValueError("Can't write to input port")
        if self.address_register == self.output_address:
            self.output_buffer += [self.data_register]
        else:
            self.memory[Address(self.address_register)] = self.data_register

    def hlt(self) -> None:
        raise HltError

    def __repr__(self):
        """Вернуть строковое представление состояния процессора."""

        value = self.memory[Address(self.program_counter)]
        rsp = self.registers[Registers.Registers.RSP]
        memory_slice = str([self.memory[Address(i)] for i in range(700, 720)])
        registers = " ".join(f"{r.name}={v}" for r, v in self.registers.registers_value.items())
        if isinstance(value, Instruction):
            opcode = value.opcode
            instr_repr = str(opcode.name)

            for term in value.terms:
                instr_repr += f" {term.value.name}"

            i = 1
            while isinstance(self.memory[Address(self.program_counter + i)], int) and opcode != Opcode.HLT:
                instr_repr += f" {self.memory[Address(self.program_counter + i)]}"
                i += 1

            state_repr = f"TICK: {self.tick:4} PC: {self.program_counter:3} SP: {rsp:4} INSTR: {instr_repr:3} REGS: {registers}"
        else:
            state_repr = f"TICK: {self.tick:4} PC: {self.program_counter:3} SP: {rsp:4} VALUE: {value:3} REGS: {registers}"

        return state_repr


def from_bytes(binary_code) -> list[Instruction | int]:
    """Преобразует бинарное представление машинного кода в структурированный формат."""
    structured_code = []
    # Обрабатываем байты по 4 за раз для получения 32-битных инструкций
    i = 0
    while i + 3 < len(binary_code):

        # Формируем 32-битное слово из 4 байтов
        binary_instr = (
            (binary_code[i] << 24) | (binary_code[i + 1] << 16) | (binary_code[i + 2] << 8) | binary_code[i + 3]
        )
        # Извлекаем опкод (старшие 10 бит)
        opcode_bin = (binary_instr >> 22)
        opcode = Opcode(opcode_bin)

        terms = []
        for j in range(OPCODE_TO_TERMS_AMOUNT[opcode][0]):
            value = binary_instr >> (19  - (j * 3)) & 0b111
            terms += [Term(Registers.Registers(value))]

        structured_code.append(Instruction(opcode, terms))

        for _ in range(OPCODE_TO_TERMS_AMOUNT[opcode][1]):
            i += 4
            binary_instr = (
                (binary_code[i] << 24) | (binary_code[i + 1] << 16) | (binary_code[i + 2] << 8) | binary_code[i + 3]
            )
            structured_code.append(binary_instr)

        i += 4

    return structured_code

def from_bytes_data(binary_data) -> list[int]:
    res = []
    i = 0
    while i + 3 < len(binary_data):
        binary_value = (
            (binary_data[i] << 24) | (binary_data[i + 1] << 16) | (binary_data[i + 2] << 8) | binary_data[i + 3]
        )
        res += [binary_value]
        i += 4
    return res



def simulation(input_address, output_address, code, data, input_tokens, is_char_io) -> str:
    datapath = DataPath(input_address, output_address)
    for i, instr in enumerate(code):
        datapath.memory[Address(i)] = instr
    for i, value in enumerate(data):
        datapath.memory[Address(i + 200)] = value

    datapath.input_buffer = input_tokens

    while datapath.tick < MAX_CYCLES:
        try:
            datapath.control_unit.run_single_micro()
        except HltError:
            logging.debug("HLT")
            break
        logging.debug(str(datapath))
    else:
        logging.error("Cycle limit hit")

    if is_char_io:
        return "".join(chr(val) for val in datapath.output_buffer).encode().decode("unicode_escape")
    return " ".join(str(val) for val in datapath.output_buffer)

def main(code_file, data_file, input_file, input_address, output_address, is_char_io) -> None:
    with open(code_file, "rb") as f:
        bin_code = f.read()
    with open(data_file, "rb") as f:
        bin_data = f.read()
    with open(input_file) as f:
        input_text = f.read()

    if is_char_io:
        input_tokens = [ord(ch) for ch in input_text + "\0"]
    elif input_text != "":
        input_tokens = [int(num) for num in input_text.split("\n")]
    else:
        input_tokens = []

    code = from_bytes(bin_code)
    data = from_bytes_data(bin_data)

    output = simulation(input_address, output_address, code, data, input_tokens, is_char_io)
    print(output)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    _, code, data, inp, char_io = sys.argv
    main(code, data, inp, 400, 401, is_char_io=int(char_io))
    # main("trash/out.bin", "trash/out.bin_data.bin", "trash/input.txt", 400, 401, is_char_io=False)
