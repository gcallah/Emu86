from .arithmetic import Add, Sub, Mul, Div_S, Div_U
from assembler.tokens import DataType

key_words = {
    # data types
    'i32': DataType('i32'),

    # arithmetic
    '.add': Add('.add'),
    '.sub': Sub('.sub'),
    '.mul': Mul('.mul'),
    '.div_s': Div_S('.div_s'),
    '.div_u': Div_U('.div_u'),
}
