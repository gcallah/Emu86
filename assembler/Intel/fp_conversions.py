from __future__ import print_function
from collections import namedtuple
from fractions import Fraction
import struct

DEFAULT_SIZE = (11, 52)


def trunc_round(n, k):
    rshift = n.bit_length() - 1 - k
    if rshift >= 0:
        n >>= (rshift)
    else:
        n <<= (-rshift)
    return (n + 1) >> 1


def more_bin_digits(n, k):
    return bool(n >> k)


def unset_high_bit(n):
    assert n > 0
    return n ^ (1 << (n.bit_length() - 1))


def fbin(n, nbits):
    assert (0 <= n)
    assert not (n >> nbits)
    return "{val:0>{width}}".format(val=bin(n)[2:], width=nbits)


_anyfloat = namedtuple("anyfloat", "sign exponent significand")


class anyfloat(_anyfloat):
    _anyfloat.sign = None
    _anyfloat.exponent = None
    _anyfloat.significand = None
    _b32 = 1 << 32
    _b64 = 1 << 64

    def __new__(cls, sign, exponent, significand):
        assert sign in (0, 1)
        if significand:
            significand = significand//(significand & -significand)
        _anyfloat.sign = sign
        _anyfloat.exponent = exponent
        _anyfloat.significand = significand

        return _anyfloat.__new__(cls, sign, exponent, significand)

    @staticmethod
    def _encode(log2, mantissa, a, b):
        A = ~(~0 << a)
        AA = A >> 1
        if mantissa <= 0:
            return ((A, 0) if (mantissa == -1)
            else (A, 1 << (b-1))) if mantissa else (0, 0)
        elif log2 <= - AA:
            nbits = b + log2 + AA
            rounded = trunc_round(mantissa, nbits) if (nbits >= 0) else 0
            return (1, 0) if more_bin_digits(rounded, b) else (0, rounded)
        elif log2 <= AA:
            rounded = trunc_round(mantissa, b + 1)
            return (((log2 + 1 + AA, 0) if (log2 < AA) else (A, 0))
            if more_bin_digits(rounded, b+1)
            else (log2 + AA, unset_high_bit(rounded)))
        else:
            return (A, 0)

    @staticmethod
    def _decode(exponent, significand, a, b):
        A = ~(~0 << a)
        AA = A >> 1
        assert 0 <= exponent <= A
        assert 0 <= significand < (1 << b)
        if exponent == A:
            return (0, -2 if significand else -1)
        elif exponent:  # normal case
            return (exponent - AA, significand | (1 << b))
        else:  # subnormal case
            if significand:
                return (significand.bit_length() - AA - b, significand)
            else:
                return (0, 0)

    def __float__(self):
        return self.int64_to_float(self.to_ieee())

    @classmethod
    def from_float(cls, x):
        """Create an anyfloat instance from a python float
        (64 bits double precision number)."""
        return cls.from_ieee(cls.float_to_int64(x))

    @classmethod
    def from_ieee(cls, n, size=DEFAULT_SIZE):
        """Create an anyfloat from an ieee754 integer.

        Create an anyfloat from an integer which binary
        representation is the ieee754
        format of a floating point number.
        The argument 'size' is a tuple (w, p)
        containing the width of the exponent part
        and the significand part in
        this ieee754 format."""
        w, p = size
        r = n >> p
        significand = (r << p) ^ n
        sign = int(r >> w)
        if sign not in (0, 1):
            raise ValueError(("Integer value out of range", n, size))
        exponent = (sign << w) ^ r
        e, s = cls._decode(exponent, significand, w, p)
        if e == -2:
            sign = 0
        _anyfloat.sign = sign
        _anyfloat.exponent = exponent
        _anyfloat.significand = significand
        return cls(sign, e, s)

    def ieee_parts(self, size=DEFAULT_SIZE):
        w, p = size
        e, s = self._encode(self.exponent, self.significand, w, p)
        sign = 0 if (e + 1) >> w else self.sign

        return [sign, e, s]

    def abs_sign(self):
        self.sign = 0
        """changes sign to  0 (positive)"""

    def change_sign(self):
        if self.sign == 0:
            self.sign = 1
        else:
            self.sign = 0

    def to_ieee(self, size=DEFAULT_SIZE):
        """Convert to an ieee754 integer.

        Convert self to an integer which binary representation
        is the ieee754 format corresponding
        to the 'size' argument (read the documentation of from_ieee()
        for the meaning of the size
        argument.
        """
        sign, e, s = self.ieee_parts(size)
        return (((sign << size[0]) | e) << size[1]) | s

    @classmethod
    def int64_to_float(cls, n):
        """Convert a 64 bits integer to a python float.

        This class method converts an integer representing a
        64 bits floating point
        number in the ieee754 double precision
        format to this floating point number."""

        if not (0 <= n < cls._b64):
            raise ValueError(("Integer value out of range", n))
        u, v = divmod(n, cls._b32)
        return struct.unpack(">d", struct.pack(">LL", u, v))[0]

    @classmethod
    def float_to_int64(cls, x):
        """Convert a python float to a 64 bits integer.

        This class method converts a float to an integer representing this
        float in the 64 bits ieee754 double precision format."""

        u, v = struct.unpack(">LL", struct.pack(">d", x))
        return (u << 32) | v

    def bin(self, size=DEFAULT_SIZE, sep=' '):
        """Return a binary representation of self.

        The returned string contains only the characters
        '0' and '1' and shows the ieee754 representation
        of the real number corresponding to self whith the given
        size = (w, p).
        """
        if sep:
            sign, e, s = self.ieee_parts(size)
            signVal = fbin(sign, 1)
            expoVal = fbin(e, size[0])
            mantissaVal = fbin(s, size[1])
            return sep.join(signVal, expoVal, mantissaVal)
        else:
            return fbin(self.to_ieee(size), sum(size) + 1)

    def to_fraction(self):
        s = self.significand
        b = s.bit_length()
        k = self.exponent + 1 - b
        if k < 0:
            d = Fraction(s, 2 ** (-k))
        else:
            d = Fraction(s * 2**k, 1)
        return -d if self.sign else d
def binaryAdd(bin1,bin2):
    additionBin = ""
    carryOver = 0
    i = -1
    while i!=(len(bin1)*-1)-1:
        if bin1[i]=='.':
            additionBin='.'+additionBin
            i-=1
            continue
        sum = int(bin1[i]) + int(bin2[i]) + carryOver
        if sum == 1 or sum == 0:
            additionBin = str(sum) + additionBin
            carryOver = 0
        elif sum == 2:
            additionBin = str(0) + additionBin
            carryOver = 1
        else:
            additionBin = str(1) + additionBin
            carryOver = 1
        i-=1
    if carryOver!=0:
        additionBin = str(carryOver) + additionBin
    return additionBin
def convertFraction(mantissa):
    product = 0
    for i in range(len(mantissa)):
        product += (int(mantissa[i])*(2**(-i-1)))
    return product
def convertFromIEE(IEEE):
    print("IEEE", IEEE)
    bits = IEEE.split(" ")
    sign, expo, mantissa = bits[0], bits[1], bits[2]

    fraction = convertFraction(mantissa)
    print(fraction)
    print(expo)
    float = (1+ fraction) * (2**(int(expo,2)))
    if sign == '0':
        return float
    return -1*float
def add(val1,val2):
    if val2 > val1:
        val1,val2 = val2, val1
    X1 = anyfloat.from_float(val1)
    sign1,expo1,mantissaBin1 = X1.sign, X1.exponent, X1.bin(size=(8,23)).split(" ")[2]
    X2 = anyfloat.from_float(val2)
    sign2,expo2,mantissaBin2 = X2.sign, X2.exponent, X2.bin(size=(8,23)).split(" ")[2]
    expoDiff = expo1 - expo2
    print(expo1, expo2)
    print("expo",expoDiff)
    if expoDiff > 0:
        allignedMant2 = "1"+mantissaBin2
        for i in range(expoDiff-1):
            allignedMant2 = "0"+allignedMant2
            allignedMant2 = allignedMant2[:-1]
        allignedMant2 = "0."+allignedMant2
        allignedMant2 = allignedMant2[:-1]
    else:
        allignedMant2 = "1."+mantissaBin2
    allignedMant1 = '1.'+mantissaBin1
    if sign1 == sign2: #add
        allignedMant3 = binaryAdd(allignedMant1,allignedMant2)
    decimalPlace = allignedMant3.find(".")
    IEEE = str(sign1) + " " + bin(expo1) + " " + allignedMant3[decimalPlace+1:]
    print(IEEE)
    return convertFromIEE(IEEE)
