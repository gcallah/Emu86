import argparse
from assembler.assemble import assemble
from assembler.virtual_machine import intel_machine, mips_machine
from assembler.virtual_machine import riscv_machine


def convert_reg_contents(registers):
    for reg in registers:
        hex_list = hex(int(registers[reg])).split('x')
        hex_list[1] = hex_list[1].upper()
        if "-" in hex_list[0]:
            registers[reg] = "-" + hex_list[1]
        else:
            registers[reg] = hex_list[1]


def convert_mem_contents(memory):
    for loc in memory:
        hex_list = hex(int(memory[loc])).split('x')
        hex_list[1] = hex_list[1].upper()
        if "-" in hex_list[0]:
            memory[loc] = "-" + hex_list[1]
        else:
            memory[loc] = hex_list[1]


def convert_stack_contents(stack):
    for loc in stack:
        hex_list = hex(int(stack[loc])).split('x')
        hex_list[1] = hex_list[1].upper()
        if "-" in hex_list[0]:
            stack[loc] = "-" + hex_list[1]
        else:
            stack[loc] = hex_list[1]


def display_results(last_instr, error, vm):
    if vm.base == "hex":
        convert_stack_contents(vm.stack)
        convert_mem_contents(vm.memory)
        convert_reg_contents(vm.registers)
    print("Last instruction: ", last_instr)
    print("Error: ", error)
    print("\nRegisters:")
    if vm.flavor == "intel" or vm.flavor == "att":
        for reg in vm.registers:
            print("\t" + reg + ": " + str(vm.registers[reg]) + "\t")
    else:
        count = 0
        for reg in vm.registers:
            if reg[0] == "F":
                continue
            print("\t" + reg + ":" + str(vm.registers[reg]) + "\t", end="")
            if reg == "R20":
                print()
                count += 2
            else:
                count += 1
                if count % 3 == 0:
                    print()
    print()
    print("\nMemory: ")
    for mem in vm.memory:
        print("\t" + mem + ": " + str(vm.memory[mem]))


def reset_vms():
    intel_machine.re_init()
    mips_machine.re_init()
    riscv_machine.re_init()
    intel_machine.flavor = None
    mips_machine.flavor = None
    riscv_machine.flavor = None
    intel_machine.base = None
    mips_machine.base = None
    riscv_machine.base = None


def run_assemble(vm, base, code):
    if vm.flavor == "intel" or vm.flavor == "att":
        if base is None:
            base = "dec"
    else:
        if base is None:
            base = "hex"
    vm.base = base
    (last_instr, error, bit_code) = assemble(code, vm.flavor, vm)
    display_results(last_instr, error, vm)


def main():
    global intel_machine
    global mips_machine
    global riscv_machine
    reset_vms()
    base = None
    parser = argparse.ArgumentParser()
    parser.add_argument("-I", help="flavor: Intel", action="store_true")
    parser.add_argument("-A", help="flavor: AT&T", action="store_true")
    parser.add_argument("-MASM", help="flavor: MIPS_ASM", action="store_true")
    parser.add_argument("-MMML", help="flavor: MIPS_MML", action="store_true")
    parser.add_argument("-R", help="flavor: RISCV", action="store_true")

    parser.add_argument("-x", help="base: hex", action="store_true")
    parser.add_argument("-d", help="base: decimal", action="store_true")

    parser.add_argument("file", help="file path of asm file")

    args = parser.parse_args()

    vm = None
    if args.I:
        intel_machine.flavor = "intel"
        vm = intel_machine
    elif args.A:
        intel_machine.flavor = "att"
        vm = intel_machine
    elif args.MASM:
        mips_machine.flavor = "mips_asm"
        vm = mips_machine
    elif args.MMML:
        mips_machine.flavor = "mips_mml"
        vm = mips_machine
    elif args.R:
        riscv_machine.flavor = "riscv"
        vm = riscv_machine
    else:
        return

    if args.x:
        base = "hex"
    elif args.d:
        base = "dec"

    file_nm = args.file
    asm_file = open(file_nm, "r")
    code = ""
    for line in asm_file:
        code += line

    run_assemble(vm, base, code)


main()
