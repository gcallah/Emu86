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
	while True:
		answer = input("Flavor Choice: ")
		if answer in flavors:
			return answer
		else:
			print("Invalid flavor choice. Try again!")

def select_numsys():
	while True:
		answer = input("Number system choice: ")
		if answer in numsys:
			return answer
		else:
			print("Invalid number system choice. Try again!")

def start():
	loop = True
	flavor = None
	base = None
	while True: 
		print("Welcome to Emu's command line assembler.\n")
		print("Please select your flavor:\n")
		print("\t1: Intel\n")
		print("\t2: AT&T\n")
		print("\t3: MIPS Assembly\n")
		print("\t4: MIPS Mnemonic Machine Language\n")
		flavor = flavors[select_flavor()]
		print("Please select your number system:\n")
		print("\t1: Decimal\n")
		print("\t2: Hexadecimal\n")
		base = numsys[select_numsys()] 
		break


def main():
	start()

main()