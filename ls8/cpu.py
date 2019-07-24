"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

        self.branchtable = {}
        self.branchtable[int(0b10100000)] = self.handle_ADD
        self.branchtable[int(0b10100011)] = self.handle_SUB
        self.branchtable[int(0b10100010)] = self.handle_MUL
        self.branchtable[int(0b10100011)] = self.handle_DIV
        # self.branchtable[int(0b01001000)] = self.handle_PRA
        self.branchtable[int(0b01000111)] = self.handle_PRN
        self.branchtable[int(0b10000010)] = self.handle_LDI
        # self.branchtable[int(0b00000001)] = self.handle_HLT

    def handle_ADD(self, operand_a, operand_b):     #  ADD
        self.alu("ADD", operand_a, operand_b)
        self.pc += 3
    def handle_SUB(self, operand_a, operand_b):     # Subtract
        self.alu("SUB", operand_a, operand_b)
        self.pc += 3
    def handle_MUL(self, operand_a, operand_b):     # Multiply
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3
    def handle_DIV(self, operand_a, operand_b):     # Divide
        self.alu("DIV", operand_a, operand_b)
        self.pc += 3

    # def handle_PRA(self, operand_a, operand_b):     #

    def handle_PRN(self, operand_a, operand_b):     # Print number in register
        print(f'{self.register[operand_a]}')
        self.pc += 2
    def handle_LDI(self, operand_a, operand_b):     # LDI:
        self.register[operand_a] = operand_b
        self.pc += 3

    def dispatch(self, IR, opA, opB):
        self.branchtable[IR](opA, opB)

    def load(self):
        """Load a program into memory."""



        if len(sys.argv) is not 2:
            print(f"usage: {sys.argv[0]} <filename>")
            sys.exit(1)

        try:
            address = 0
            program_name = sys.argv[1]

            with open(program_name) as f:
                for line in f:
                    num = line.split("#", 1)[0]

                    if num.strip() == '':  # ignore comment-only lines
                        continue
                    num = '0b' + num
                    # print(num)
                    self.ram[address] = int(num, 2)
                    address += 1

            print(self.ram)

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit(2)

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value
        pass

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "SUB":
            self.register[reg_a] -= self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        elif op == "DIV":
            self.register[reg_a] /= self.register[reg_b]
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

            IR = self.pc
            operand_a = self.ram_read(IR + 1)
            operand_b = self.ram_read(IR + 2)
            if self.ram[IR] == int(0b00000001):               # HLT base case: exit loop
                running = False
            else:
                # print(self.ram[IR])
                self.dispatch(self.ram[IR], operand_a, operand_b)
