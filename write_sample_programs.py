import os

link_names = {
    "power.asm": "Raise a number to a power",
    "array.asm": "Declare an array",
    "sum_test.asm": "Add two numbers",
    "key_test.asm": "Uses our keyboard interrupt",
    "arithmetic_shift.asm": "Arithmetic shift",
    "area.asm": "Calculate area of a rectangle",
    "loop.asm": "A simple loop",
    "mem_register_test.asm": "Store values into memory",
    "log.asm": "Calculate log in base 2",
    "arithmetic_expression.asm": "Calculate an arithmetic expression",
    "cel_to_fah.asm": "Convert from Celsius to Fahrenheit",
    "data.asm": "How to use the .data section",
    "array_average_test.asm": "Calculate average of an array of numbers",
    "change_array_elem_test.asm": "Change array elements below min",
    "int_square_root.asm": "Calculate square root of a number",
    "reg_mem_addition_test.asm": "Store values into memory using multi syntax"
}


def create_href():
    tab = '    '
    directories = [
                    "tests/Intel",
                    "tests/ATT",
                    "tests/MIPS_ASM",
                    "tests/MIPS_MML",
                    "tests/RISCV"
                    ]
    for dire in directories:
        directory_intel = os.fsencode(dire)
        name = "templates/sample_programs"
        if dire == "tests/Intel":
            name += "_intel"
        elif dire == "tests/ATT":
            name += "_att"
        elif dire == "tests/MIPS_ASM":
            name += "_mips_asm"
        elif dire == "tests/MIPS_MML":
            name += "_mips_mml"
        else:
            name += "_riscv"
        file_name = open(name + ".txt", "w")
        file_name.write(tab * 3 + '<ul class="nested">\n')
        for file in os.listdir(directory_intel):
            file = os.fsdecode(file)
            if file.endswith(".asm") and file in link_names:
                file_name.write(tab * 4 + "<li>\n")
                file_name.write(tab * 5 +
                                '<a href ="https://github.com/gcallah/' +
                                "Emu86/blob/master/" + dire + "/" +
                                file + '">\n')
                file_name.write(tab * 6 + link_names[file] + "\n")
                file_name.write(tab * 5 + "</a>\n")
                file_name.write(tab * 4 + "</li>\n")
        file_name.write(tab * 3 + "</ul>\n")
        file_name.close()


def create_sidebar():
    tab = '    '
    directory = os.fsencode("tests/Intel")
    file_name = open("templates/samples.txt", "w")
    file_name.write(tab * 3 +
                    '<ul class="collapse list-unstyled nested"' +
                    ' id="programsSubmenu">\n')
    for file in os.listdir(directory):
        file = os.fsdecode(file)
        if file.endswith(".asm") and file in link_names:
            file_name.write(tab * 4 + "<li>\n")
            file_name.write(tab * 5 +
                            '<a href ="' + file[:len(file) - 3] +
                            'html">\n')
            file_name.write(tab * 6 + link_names[file] + "\n")
            file_name.write(tab * 5 + "</a>\n")
            file_name.write(tab * 4 + "</li>\n")
    file_name.write(tab * 3 + "</ul>\n")
    file_name.close()


def main():
    create_href()
    create_sidebar()


main()
