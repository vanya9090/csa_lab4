import assembler
from machine.machine import Address, DataPath

# SRC = """
#     MOV R0, #5     ; load literal
#     MOV R1, R0     ; copy
#     INC R1
#     DEC R0
#     STORE R1, 9
#     STORE R1, R1
# """

# SRC = """
# MOV R0, #100       ; 0: loop counter
# MOV R1, #0       ; 2: accumulator
# MOV R2, R0       ; 4: temp copy of R0
# STORE R2, 20     ; 5: store R0 → mem[20] for ADD
# ADD R1, R!, 20    ; 7: R1 += mem[20]
# DEC R0           ; 9: R0 -= 1
# BEQZ R0, 14      ; 10: if R0 == 0 → jump to STORE
# JMP 4            ; 12: jump to MOV R2, R0 (line 4)
# STORE R1, 19     ; 14: store result (15) in mem[0]
# """

# SRC = """
# MOV RSP, #200      ; initialize stack pointer
# MOV R0, #3         ; countdown from 3

# CALL 6             ; call addr 6 (loop start)

# JMP 11             ; skip function after call

# DEC R0             ; addr 6: function body
# BEQZ R0, 10        ; if zero, jump to RET
# CALL 6             ; recurse
# RET                ; addr 10

# """

PROGRAM_OFFSET = 0

words = assembler.assemble_program(SRC)
for word in words:
    print(word)

dp = DataPath(input_address=0, output_address=0)
for addr, w in enumerate(words):
    dp.memory[Address(addr + PROGRAM_OFFSET)] = w
print(f"Program size: {len(words)} words")

dp.program_counter = PROGRAM_OFFSET
MAX_CYCLES = 1_000
for cycle in range(MAX_CYCLES):
    dp.control_unit.run_single_micro()
    if dp.program_counter >= len(words) + PROGRAM_OFFSET:
        print(f"\nProgram finished after {cycle + 1} micro-cycles.")
        break
else:
    print("cycle limit hit")

print("\nRegister file:")
for r, v in dp.registers.registers_value.items():
    print(f"  {r.name:3} = {v}")

print("\nMemory:")
for i in range(20):
    print(dp.memory[Address(i)])
