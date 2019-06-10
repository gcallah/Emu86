from .arithmetic import Add, Sub, Mul, Div_S, Div_U
from .arithmetic import Rem_S, Rem_U, And, Or, Xor
from .arithmetic import Shl, Shr_S, Shr_U, Rotl, Rotr
from .arithmetic import Clz, Ctz, Popcnt, Eqz
from .data_mov import Global_set, Local_set, Store_global, Store_local
from .data_mov import Global_get, Local_get, Store_const
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
    'i32.rem_s': Rem_S('.rem_s'),
    'i32.rem_u': Rem_U('.rem_u'),
    'i32.and': And('.and'),
    'i32.or': Or('.or'),
    'i32.xor': Xor('.xor'),
    'i32.shl': Shl('.shl'),
    'i32.shr_s': Shr_S('.shr_s'),
    'i32.shr_u': Shr_U('.shr_u'),
    'i32.rotl': Rotl('.rotl'),
    'i32.rotr': Rotr('.rotr'),
    'i32.clz': Clz('.clz'),
    'i32.ctz': Ctz('.ctz'),
    'i32.popcnt': Popcnt('.popcnt'),
    'i32.eqz': Eqz('.eqz'),

    # data movement
    'global.get': Global_get('global.get'),
    'local.get': Local_get('local.get'),
    'global.set': Global_set('global.set'),
    'local.set': Local_set('local.set'),
    'global': Store_global('global'),
    'local': Store_local('local'),
    'i32.const': Store_const('i32.const')
}
