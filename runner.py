from machine import DataPath, ControlUnit
from isa import Instruction, Opcode
import assembler

# SRC = """
#     MOV R0, #5     ; load literal
#     MOV R1, R0     ; copy
#     INC R1
#     DEC R0
#     STORE R1, 9
#     STORE R1, R1
# """

SRC = """
MOV R0, #10
MOV R1, #20

MOV R2, R0
MOV R3, R1

INC R2
DEC R3

STORE R2, 0
STORE R3, 1

INC 0
DEC 1

MOV R4, [0]
MOV R5, [1]

MOV R6, #5
STORE R0, R6
MOV R7, [R6]

ADD 3, R0, 1, 0, 5
"""

PROGRAM_OFFSET = 100

words = assembler.assemble_program(SRC)
for word in words:
    print(word)

dp = DataPath(input_address=0, output_address=0)
for addr, w in enumerate(words):
    dp.memory[addr + PROGRAM_OFFSET] = w
print(f"Program size: {len(words)} words")

dp.control_unit.program_counter = PROGRAM_OFFSET
MAX_CYCLES = 1000
for cycle in range(MAX_CYCLES):
    dp.control_unit.run_single_micro()
    if dp.control_unit.program_counter >= len(words) + PROGRAM_OFFSET:
        print(f"\nProgram finished after {cycle+1} micro-cycles.")
        break
else:
    print("cycle limit hit")

print("\nRegister file:")
for r, v in dp.registers.registers_value.items():
    print(f"  {r.name:3} = {v}")

print("\nMemory:")
for i in range(10):
    print(dp.memory[i])
