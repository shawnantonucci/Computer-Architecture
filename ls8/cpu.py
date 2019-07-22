"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.memory = [0] * 256
        self.register = [0] * 8
        self.IR = 0
        self.PC = 0
        self.MDR = 0
        self.MAR = 0

    def ram_read(self, MAR):
        return self.memory[MAR]

    def ram_write(self, MDR, MAR):
        self.memory[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.memory[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        running = True

        while running:
            self.IR = self.PC
            operand_a = self.ram_read(self.IR + 1)
            operand_b = self.ram_read(self.IR + 2)
            # print("Loop")

            if self.memory[self.IR] == 0b00000001:
                running = False

            elif self.memory[self.IR] == 0b10000010:
                self.register[operand_a] = operand_b
                # print("LDI")
                self.PC += 3

            elif self.memory[self.IR] == 0b01000111:
                print(self.register[operand_a])
                # print("PRN")
                self.PC += 2

# cpu = CPU()
# # cpu.ram_write(20, 0)
# print(cpu.memory)
# # print(cpu.trace)
# # print(cpu.ram_read(0))
# cpu.load()
# cpu.run()
