import os 

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

def create_js_file():
	tab = '\t'
	intel_directory = ["tests/Intel/", "tests/ATT/"]
	js_file = open("mysite/static/Emu86/helper_functions.js", "w")
	file_code = function_directory(function_names, intel_directory + ["tests/MIPS/"])
	file_code += function_directory(intel_function_names, intel_directory)
	js_file.write(file_code)
	js_file.close()


def main():
	create_js_file()

main()
