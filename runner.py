from machine import DataPath, ControlUnit
from isa import Instruction, Opcode
import assembler

SRC = """
    MOV R0, #5     ; load literal
    MOV R1, R0     ; copy
    INC R1          
    DEC R0
"""

words = assembler.assemble_program(SRC)
for word in words:
    print(word)

dp = DataPath(input_address=0, output_address=0)
for addr, w in enumerate(words):
    dp.memory[addr] = w
print(f"Program size: {len(words)} words")

MAX_CYCLES = 1000
for cycle in range(MAX_CYCLES):
    dp.control_unit.run_single_micro()
    if dp.control_unit.program_counter >= len(words):
        print(f"\nProgram finished after {cycle+1} micro-cycles.")
        break
else:
    print("cycle limit hit")

print("\nRegister file:")
for r, v in dp.registers.registers_value.items():
    print(f"  {r.name:3} = {v}")
