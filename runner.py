from machine.machine import DataPath, ControlUnit
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
MOV R0, #21     ; 0
MOV R1, #0     ; 2
DEC R0         ; 4
INC R1         ; 5
BEQZ R0, 10    ; 6, 7
JMP 4          ; 8, 9
STORE R1, 0    ; 10, 11
"""

PROGRAM_OFFSET = 0

words = assembler.assemble_program(SRC)
for word in words:
    print(word)

dp = DataPath(input_address=0, output_address=0)
for addr, w in enumerate(words):
    dp.memory[addr + PROGRAM_OFFSET] = w
print(f"Program size: {len(words)} words")

dp.program_counter = PROGRAM_OFFSET
MAX_CYCLES = 10_000
for cycle in range(MAX_CYCLES):
    dp.control_unit.run_single_micro()
    if dp.program_counter >= len(words) + PROGRAM_OFFSET:
        print(f"\nProgram finished after {cycle+1} micro-cycles.")
        break
else:
    print("cycle limit hit")

print("\nRegister file:")
for r, v in dp.registers.registers_value.items():
    print(f"  {r.name:3} = {v}")

print("\nMemory:")
for i in range(20):
    print(dp.memory[i])
