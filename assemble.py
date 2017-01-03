"""
assemble.py
Executes assembly code typed in.
"""

def move(code):
    pass

def add(code):
    pass

instructions = {
        'MOV': move,
        'ADD': add,
        }

def assemble(code, registers):  # memory to come!
    """
        Assembles and runs code.
        Args:
            code: code to assemble.
            registers: current register values.
        Returns:
            Output, if any.
            Error, if any.
    """
    output = ''
    error = ''
#    while len(code) > 0:
    token = get_token(code)
    if token not in instructions:
        return (output, "Invalid instruction.")
        code = code[len(token) + 1:]
    return ("Got token of: " + token, '')

def get_token(code):
    """
        Gets the next token.
        Args:
            The string of code, set to current pos.
        Returns:
            The next token from string.
    """
    token = ''
    for char in code:
        if char != ',' and char != ' ':
            token = token + char
        else:
            break
    return token
