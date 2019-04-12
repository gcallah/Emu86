from .arithmetic import Add, Sub, Mul, Div_S, Div_U
from .data_mov import Global_mov, Local_mov, Store_global, Store_local
from assembler.tokens import DataType

key_words = {
    # data types
    'i32': DataType('i32'),

    # arithmetic
    'i32.add': Add('.add'),
    'i32.sub': Sub('.sub'),
    'i32.mul': Mul('.mul'),
    'i32.div_s': Div_S('.div_s'),
    'i32.div_u': Div_U('.div_u'),
    'global.get': Global_mov('global.get'),
    'local.get': Local_mov('local.get'),
    'global': Store_global('global'),
    'local': Store_local('local')
}
