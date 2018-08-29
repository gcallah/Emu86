import os 
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
}

intel_function_names = {
	"key_test.asm": "keyInterrupt",
	"mem_register_test.asm": "dataAccess"
}

INTEL = 0
ATT = 1
MIPS = 2

def convert_line_dec(code):
	dec_num = re.compile(r'\d+')
	match_lst = dec_num.findall(code)
	for match in match_lst:
		start = code.find(match)
		end = start + len(match)
		dec_string = int(code[start:end])
		hex_string = hex(dec_string)
		hex_lst = hex_string.split('0x')
		hex_lst[-1] = hex_lst[-1].upper()
		hex_string = "0x".join(hex_lst)
		code = code[:start] + hex_string + code[end:]
	return code

def function_directory(func_dict, directory_lst):
	file_code = ""
	for file_name in func_dict:
		function_code = ""
		count = 0
		function_code += "function " + func_dict[file_name] + "(flavor) {"
		function_code += "\n\tcode_string = '';" 
		for dire in directory_lst:
			sample_test = open(dire + file_name, "r")
			if count == 0: 
				function_code += "\n\tif (flavor == 'intel'){\n"
			elif count == 1:
				function_code += "\n\telse if (flavor == 'att'){\n"
			else:
				function_code += "\n\telse{\n"	

			function_code += "\t\tcode_string += " + repr(sample_test.read())
			sample_test.close()
			function_code += ";\n\t}"
			count += 1
		function_code += "\n\tdocument.getElementById('id_code')" 
		function_code += ".value = code_string;\n}"
		file_code += function_code + "\n"
	return file_code

def function_directory_hex(func_dict, directory_lst):
	file_code = ""
	for file_name in func_dict:
		function_code = ""
		count = 0
		function_code += "function " + func_dict[file_name] + "_hex(flavor) {"
		function_code += "\n\tcode_string = '';" 
		for dire in directory_lst:
			sample_test = open(dire + file_name, "r")
			if count == 0: 
				function_code += "\n\tif (flavor == 'intel'){\n"
			elif count == 1:
				function_code += "\n\telse if (flavor == 'att'){\n"
			else:
				function_code += "\n\telse{\n"	

			function_code += "\t\tcode_string += " 
			if count == 2:
				function_code += repr(sample_test.read())
			else:
				for line in sample_test:
					if line.strip() == "":
						function_code += repr(line)
					elif line.strip()[0] == ";":
						function_code += repr(line)
					else:
						function_code += repr(convert_line_dec(line))
			sample_test.close()
			function_code += ";\n\t}"
			count += 1
		function_code += "\n\tdocument.getElementById('id_code')" 
		function_code += ".value = code_string;\n}"
		file_code += function_code + "\n"
	return file_code

def create_js_file():
	tab = '\t'
	intel_directory = ["tests/Intel/", "tests/ATT/"]
	js_file_dec = open("mysite/static/Emu86/helper_functions.js", "w")
	file_code = function_directory(function_names, intel_directory + ["tests/MIPS/"])
	file_code += function_directory(intel_function_names, intel_directory)
	js_file_dec.write(file_code)
	js_file_dec.close()

	js_file_hex = open("mysite/static/Emu86/helper_functions_hex.js", "w")
	file_code = function_directory_hex(function_names, intel_directory + ["tests/MIPS/"])
	file_code += function_directory_hex(intel_function_names, intel_directory)
	js_file_hex.write(file_code)
	js_file_hex.close()


def main():
	create_js_file()

main()
