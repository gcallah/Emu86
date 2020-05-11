import re

function_names = {
    "sum_test.asm": "addTwo",
    "arithmetic_expression.asm": "arithExpr",
    "area.asm": "area",
    "power.asm": "power",
    "data.asm": "data",
    "loop.asm": "loop",
    "log.asm": "log",
    "array_average_test.asm": "avg",
    "cel_to_fah.asm": "celFah",
    "change_array_elem_test.asm": "modify",
    "int_square_root.asm": "sqrt",
    "arithmetic_shift.asm": "arithShift",
    "array.asm": "array",
    "simple_func.asm": "simpleFunc",
    "fibonacci.asm": "fibonacci"
}

intel_function_names = {
    "key_test.asm": "keyInterrupt",
    "mem_register_test.asm": "dataAccess"
}

fp_function_names = {
    "fp_area.asm": "area_fp",
    "fp_data.asm": "data_fp",
    "fp_power.asm": "power_fp",
    "fp_sum_test.asm": "addTwo_fp",
    "fp_cel_to_fah.asm": "celFah_fp"
}


INTEL_TEST_DIRS = [
    "tests/tests_Intel/", 
    "tests/tests_ATT/"
]
FP_DIRS = INTEL_TEST_DIRS + ["tests/tests_MIPS_ASM/"]
ALL_TEST_DIRS = INTEL_TEST_DIRS + [
    "tests/tests_MIPS_ASM/",
    "tests/tests_MIPS_MML/",
    "tests/tests_RISCV/",
    "tests/tests_WASM/"
]

INTEL = 0
ATT = 1
MIPS_ASM = 2
MIPS_MML = 3
RISCV = 4
WASM = 5

DEC = 0
HEX = 1
DEC_LANGS = [INTEL, ATT, WASM]


def should_convert(code, pos):
    # if already converted or is part of label name
    if code[pos - 2: pos] == "0x" or code[pos - 1: pos].isalpha():
        return False

    if pos + 2 < len(code) and code[pos: pos + 2] == "0x":
        return False
    return True


def convert_line_dec_to_hex(code):
    dec_num = re.compile(r'\d+')
    match_lst = dec_num.findall(code)
    for match in match_lst:
        start = code.find(match)
        while not should_convert(code, start):
            start = code.find(match, start + 1)
            if start == -1:
                break
        if start == -1:
            continue
        end = start + len(match)
        dec_string = int(code[start:end])
        hex_string = hex(dec_string)
        hex_lst = hex_string.split('0x')
        hex_lst[-1] = hex_lst[-1].upper()
        hex_string = "0x".join(hex_lst)
        code = code[:start] + hex_string + code[end:]
    return code


def convert_line_hex_to_dec(code):
    hex_num = re.compile(r'0x\d+[A-F]*')
    match_lst = hex_num.findall(code)
    for match in match_lst:
        start = code.find(match)
        end = start + len(match)
        dec_num = int(code[start:end], 16)
        code = code[:start] + str(dec_num) + code[end:]
    hex_num = re.compile(r'0x[A-F]+\d*')
    match_lst = hex_num.findall(code)
    for match in match_lst:
        start = code.find(match)
        end = start + len(match)
        dec_num = int(code[start:end], 16)
        code = code[:start] + str(dec_num) + code[end:]
    return code


def hex_to_float(h):
    h2 = h[2:]
    h2 = binascii.unhexlify(h2)         # noqa
    return struct.unpack('>f', h2)[0]   # noqa


def convert_line_hex_to_fp(code):
    hex_num = re.compile(r'0x\d+[A-F]*')
    match_lst = hex_num.findall(code)
    for match in match_lst:
        start = code.find(match)
        end = start + len(match)
        # fp_num = hex_to_float(code[start:end])
        fp_num = code[start:end]
        code = code[:start] + str(fp_num) + code[end:]
    hex_num = re.compile(r'0x[A-F]+\d*')
    match_lst = hex_num.findall(code)
    for match in match_lst:
        start = code.find(match)
        end = start + len(match)
        # fp_num = hex_to_float(code[start:end])
        fp_num = code[start:end]
        code = code[:start] + str(fp_num) + code[end:]
    return code


def create_function_def(file_name, func_dict, base):
    function_header = "function " + func_dict[file_name]
    if base == HEX:
        return function_header + "_hex"
    return function_header


def create_cond_line(const_val):
    lang = ""
    if const_val == INTEL:
        lang = "intel"
        return "\n\tif (flavor === '" + lang + "'){\n"
    elif const_val == ATT:
        lang = "att"
    elif const_val == MIPS_ASM:
        lang = "mips_asm"
    elif const_val == MIPS_MML:
        lang = "mips_mml"
    else:
        lang = "riscv"
    return "\n\telse if (flavor === '" + lang + "'){\n"


def sample_dir(func_dict, directory_lst, base):
    file_code = ""
    for file_name in func_dict:
        function_code = create_function_def(file_name, func_dict, base)
        count = 0
        function_code += "(flavor) {\n\tlet codeString = '';"
        for dire in directory_lst:
            if count < WASM:
                function_code += create_cond_line(count)
            else:
                if file_name != "sum_test.asm" and file_name != 'area.asm':
                    break
                function_code += "\n\telse{\n"
            sample_test = open(dire + file_name, "r")
            function_code += "\t\tcodeString += "
            if ((base == DEC and count in DEC_LANGS) or
                    base == HEX and count != 0 and count != 1 and count != 5 or
                    count == 3):
                function_code += repr(sample_test.read())
            else:
                sample_conv = ""
                for line in sample_test:
                    if line.strip() == "":
                        sample_conv += line
                    elif line.strip()[0] == ";":
                        sample_conv += line
                    else:
                        if base == DEC:
                            sample_conv += convert_line_hex_to_dec(line)
                        else:
                            sample_conv += convert_line_dec_to_hex(line)
                function_code += repr(sample_conv)
            sample_test.close()
            function_code += ";\n\t}"
            count += 1
        function_code += "\n\tdocument.getElementById('id_code')"
        function_code += ".value = codeString;\n}"
        file_code += function_code + "\n"
    return file_code


def function_directory_fp(func_dict, directory_lst):
    file_code = ""
    for file_name in func_dict:
        count = 0
        function_code = f"function {func_dict[file_name]}(flavor)"
        function_code += "{\n\tlet codeString = '';"
        for dire in directory_lst:
            sample_test = open(dire + file_name, "r")
            if count == 0:
                function_code += "\n\tif (flavor === 'intel'){"
            elif count == 1:
                function_code += "\n\telse if (flavor == 'att'){"
            else:
                function_code += "\n\telse if (flavor == 'mips_asm'){"

            function_code += "\n\t\tcodeString += "
            function_code += repr(sample_test.read())

            sample_test.close()
            function_code += ";\n\t}"
            count += 1
        function_code += "\n\tdocument.getElementById('id_code')"
        function_code += ".value = codeString;\n}"
        file_code += function_code + "\n"
    return file_code


def create_js_files():
    js_file_dec = open("mysite/static/Emu86/sample_functions.js", "w")
    file_code = sample_dir(function_names, ALL_TEST_DIRS, DEC)
    file_code += sample_dir(intel_function_names, INTEL_TEST_DIRS, DEC)
    js_file_dec.write(file_code)
    js_file_dec.close()

    js_file_hex = open("mysite/static/Emu86/sample_functions_hex.js", "w")
    file_code = sample_dir(function_names, ALL_TEST_DIRS, HEX)
    file_code += sample_dir(intel_function_names, INTEL_TEST_DIRS, HEX)
    js_file_hex.write(file_code)
    js_file_hex.close()

    js_file_fp = open("mysite/static/Emu86/sample_functions_fp.js", "w")
    file_code = function_directory_fp(fp_function_names, FP_DIRS)
    file_code += function_directory_fp(intel_function_names, INTEL_TEST_DIRS)
    js_file_fp.write(file_code)
    js_file_fp.close()


def main():
    create_js_files()


main()
