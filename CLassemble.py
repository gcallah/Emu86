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

def select_flavor():
    print("Welcome to Emu's command line assembler.")
    print("Please select your flavor:")
    print("\t1: Intel")
    print("\t2: AT&T")
    print("\t3: MIPS Assembly")
    print("\t4: MIPS Mnemonic Machine Language")
    while True:
        answer = input("Flavor Choice: ")
        if answer in flavors:
            return answer
        else:
            print("Invalid flavor choice. Try again!")

def select_numsys():
    print("Please select your number system:")
    print("\t1: Decimal")
    print("\t2: Hexadecimal")
    while True:
        answer = input("Number system choice: ")
        if answer in numsys:
            return answer
        else:
            print("Invalid number system choice. Try again!")

def obtain_file():
    while True:
        file_nm = input("Please input an asm file name to run: ")
        if file_nm[len(file_nm) - 4:] != ".asm":
            print("Invalid asm file!")
        else: 
            try: 
                asm_file = open(file_nm, "r")
                asm_file.close()
                return file_nm
            except:
                print("File not found! Try again!")

def display_results(last_instr, error, vm):
    print("Last instruction: ", last_instr)
    print("Error: ", error)
    for reg in vm.registers:
        print(reg, vm.registers[reg])
    for mem in vm.memory:
        print(mem, vm.memory[mem])


def main():
    global intel_machine
    global mips_machine
    loop = True
    flavor = None
    base = None
    last_instr = None
    error = None
    flavor = flavors[select_flavor()]
    base = numsys[select_numsys()] 
    file_nm = obtain_file()
    asm_file = open(file_nm, "r")
    code = ""
    for line in asm_file:
        code += repr(line)
    if flavor == "intel" or flavor == "att":
        intel_machine.flavor = flavor
        intel_machine.base = base
        (last_instr, error, bit_code) = assemble(code, intel_machine.flavor,
                                                 intel_machine)
        display_results(last_instr, error, intel_machine)
    else:
        mips_machine.flavor = flavor
        mips_machine.base = base
        (last_instr, error, bit_code) = assemble(code, mips_machine.flavor,
                                                 mips_machine)
        display_results(last_instr, error, mips_machine)



main()