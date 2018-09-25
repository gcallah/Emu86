import argparse
from assembler.virtual_machine import intel_machine, mips_machine
from assembler.assemble import assemble

flavors = {
    "1": "intel",
    "2": "att",
    "3": "mips_asm",
    "4": "mips_mml"
}

numsys = {
    "1": "dec",
    "2": "hex"
}

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
        for reg in vm.registers :
            if reg[0] == "F":
                continue
            print("\t" + reg + ":" + str(vm.registers[reg]) + "\t", end = "")
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


def main():
    global intel_machine
    global mips_machine
    flavor = None
    base = None
    last_instr = None
    error = None
    parser = argparse.ArgumentParser()
    parser.add_argument("-I", help = "flavor: Intel", action="store_true")
    parser.add_argument("-A", help = "flavor: AT&T", action="store_true")
    parser.add_argument("-MASM", help = "flavor: MIPS_ASM", action="store_true")
    parser.add_argument("-MMML", help = "flavor: MIPS_MML", action="store_true")

    parser.add_argument("-x", help = "base: hex", action="store_true")
    parser.add_argument("-d", help = "base: decimal", action="store_true")

    parser.add_argument("file", help = "file path of asm file")

    args = parser.parse_args()
    if args.I:
         flavor = "intel"
    elif args.A:
         flavor = "att"
    elif args.MASM:
         flavor = "mips_asm"
    elif args.MMML:
         flavor = "mips_mml"

    if args.x:
         base = "hex"
    elif args.d:
         base = "dec"

    if flavor == None or base == None:
         return

    file_nm = args.file
    asm_file = open(file_nm, "r")
    code = ""
    for line in asm_file:
        code += line
    if flavor == "intel" or flavor == "att":
        intel_machine.flavor = flavor
        intel_machine.base = base
        (last_instr, error, bit_code) = assemble(code, intel_machine.flavor,
                                                 intel_machine)
        display_results(last_instr, error, intel_machine)
    else:
        mips_machine.flavor = flavor
        mips_machine.base = base
        print (mips_machine.base)
        (last_instr, error, bit_code) = assemble(code, mips_machine.flavor,
                                                 mips_machine)
        display_results(last_instr, error, mips_machine)



main()