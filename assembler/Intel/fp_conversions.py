from __future__ import print_function
# from assembler.virtual_machine import intel_machine
from assembler.errors import DivisionZero
from collections import namedtuple
from fractions import Fraction
import struct

DEFAULT_SIZE = (11, 52)


def trunc_round(n, k):
    """
    :param n: int
    :param k: int
    :return: int after
    trunc_round(49,2) -> 3
    """
    rshift = n.bit_length() - 1 - k
    if rshift >= 0:
        n >>= (rshift)
    else:
        n <<= (-rshift)
    return (n + 1) >> 1


def more_bin_digits(n, k):
    """

    :param n: int
    :param k: int
    :return: boolean
    """
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

    _b32 = 1 << 32
    _b64 = 1 << 64

    def __new__(cls, sign, exponent, significand):
        assert sign in (0, 1)
        if significand:
            significand = significand//(significand & -significand)
        return _anyfloat.__new__(cls, sign, exponent, significand)

    @staticmethod
    def _encode(log2, mantissa, a, b):
        A = ~(~0 << a)
        AA = A >> 1
        if mantissa <= 0:
            encoded = (A, 0) if (mantissa == -1) else (A, 1 << (b-1))
            return encoded if mantissa else (0, 0)
        elif log2 <= - AA:
            nbits = b + log2 + AA
            rounded = trunc_round(mantissa, nbits) if (nbits >= 0) else 0
            return (1, 0) if more_bin_digits(rounded, b) else (0, rounded)
        elif log2 <= AA:
            rounded = trunc_round(mantissa, b + 1)
            encoded = ((log2 + 1 + AA, 0) if (log2 < AA) else (A, 0))
            if more_bin_digits(rounded, b+1):
                return encoded
            else:
                return (log2 + AA, unset_high_bit(rounded))
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
        val = cls.from_ieee(cls.float_to_int64(x))
        return val

    @classmethod
    def from_ieee(cls, n, size=DEFAULT_SIZE):
        """Create an anyfloat from an ieee754 integer.

        Create an anyfloat from an integer which binary representation
        is the ieee754 format of a floating point number.
        The argument 'size' is a tuple (w, p)
        containing the width of the exponent part and the significand part in
        this ieee754 format."""
        w, p = size
        r = n >> p
        significand = (r << p) ^ n
        sign = int(r >> w)
        if sign not in (0, 1):
            error_msg = "Integer value out of range for ieee754 format"
            raise ValueError((error_msg, n, size))
        exponent = (sign << w) ^ r
        e, s = cls._decode(exponent, significand, w, p)
        if e == -2:
            sign = 0
        cls.sign = sign
        cls.exponent = e
        cls.significand = s
        return cls(sign, e, s)

    def ieee_parts(self, size=DEFAULT_SIZE):
        w, p = size
        e, s = self._encode(self.exponent, self.significand, w, p)
        sign = 0 if (e + 1) >> w else self.sign
        return [sign, e, s]

    def abs_sign(self):
        self.sign = 0  # changes sign to  0 (positive)

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
        for the meaning of the size argument.
        """
        sign, e, s = self.ieee_parts(size)
        return (((sign << size[0]) | e) << size[1]) | s

    @classmethod
    def int64_to_float(cls, n):
        """Convert a 64 bits integer to a python float.

        This class method converts an integer
        representing a 64 bits floating point
        number in the ieee754 double precision format
        to this floating point number."""

        if not (0 <= n < cls._b64):
            error_msg = "Integer value out of range for 64 bits ieee754 format"
            raise ValueError((error_msg, n))
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

        The returned string contains only the characters '0' and '1'
        and shows the ieee754 representation of the real number
        corresponding to self within the given size = (w, p).
        """
        if sep:
            sign, e, s = self.ieee_parts(size)
            bin_left = fbin(sign, 1)
            bin_mid = fbin(e, size[0])
            bin_right = fbin(s, size[1])
            return sep.join((bin_left, bin_mid, bin_right))
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


def binaryAdd(bin1, bin2):
    additionBin = ""
    carryOver = 0
    i = -1
    while i != (len(bin1) * -1) - 1:
        if bin1[i] == '.':
            additionBin = '.' + additionBin
            i -= 1
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
        i -= 1
    if carryOver != 0:
        additionBin = str(carryOver) + additionBin
    return additionBin


def binarySubtract(val1, val2):
    """

    :param val1: binary representation of int value in String format
    :param val2: binary representation of int value in String format
    :return: binary value in string format


    """
    difference = [0 for x in val1 if x != '.']
    bin1 = [int(x) for x in val1 if x != '.']
    bin2 = [int(x) for x in val2 if x != '.']
    for i in range(1, len(bin1) + 1):
        value = (bin1[-i]) - (bin2[-i])
        if value == -1:
            j = -i
            while bin1[j] == 0:
                j -= 1
            bin1[j] -= 1
            for k in range(j + 1, -i):
                bin1[k] = 1
            bin1[-i] = 2
            value = (bin1[-i]) - (bin2[-i])
        difference[-i] = value
    difference.insert(1, '.')
    binary = ''.join(str(x) for x in difference)
    return binary


def convertFraction(mantissa):
    product = 0
    for i in range(len(mantissa)):
        product += (int(mantissa[i])*(2**(-i-1)))
    return product


def convertFromIEE(IEEE):
    bits = IEEE.split(" ")
    sign, expo, mantissa = bits[0], bits[1], bits[2]

    fraction = convertFraction(mantissa)
    float = (1 + fraction) * (2**(int(expo, 2)))
    if sign == '0':
        return float
    return -1 * float


def fabs(val):
    IEEE = anyfloat.from_float(val)
    IEEE.abs_sign()
    return float(IEEE)


def chs(val):
    IEEE = anyfloat.from_float(val)
    IEEE.change_sign()
    return float(IEEE)


# performing addition of 2  numbers
def add(val1, val2):
    val1, val2 = float(val1), float(val2)

    if abs(val2) > abs(val1):
        val1, val2 = val2, val1
    X1 = anyfloat.from_float(val1)
    sign1, expo1 = X1.sign, X1.exponent
    mantissaBin1 = X1.bin(size=(11, 52)).split(" ")[2]
    X2 = anyfloat.from_float(val2)
    sign2, expo2 = X2.sign, X2.exponent
    mantissaBin2 = X2.bin(size=(11, 52)).split(" ")[2]
    expoDiff = expo1 - expo2
    if expoDiff != 0:
        allignedMant2 = "1"+mantissaBin2
        for i in range(abs(expoDiff)-1):
            allignedMant2 = "0"+allignedMant2
            allignedMant2 = allignedMant2[:-1]
        allignedMant2 = "0."+allignedMant2
        allignedMant2 = allignedMant2[:-1]
    else:
        allignedMant2 = "1."+mantissaBin2
    allignedMant1 = '1.'+mantissaBin1
    if sign1 == sign2:  # add
        allignedMant3 = binaryAdd(allignedMant1, allignedMant2)
    else:
        allignedMant3 = binarySubtract(allignedMant1, allignedMant2)
    decimalPlace = allignedMant3.find(".")
    if decimalPlace != 1:
        expo1 += (decimalPlace - 1)
        rightSide = allignedMant3[1:decimalPlace]
        allignedMant3_left = allignedMant3[0] + "." + rightSide
        allignedMant3_right = allignedMant3[decimalPlace + 1:-len(rightSide)]
        allignedMant3 = allignedMant3_left + allignedMant3_right
    if allignedMant3[0] == '0':
        firstOne = allignedMant3.find("1")
        expo1 -= (firstOne - 1)
        allignedMant3 = allignedMant3[firstOne]+'.'+allignedMant3[firstOne+1:]
        while len(allignedMant3) < 54:
            allignedMant3 += '0'
    IEEE = str(sign1) + " " + bin(expo1) + " " + allignedMant3[2:]
    return convertFromIEE(IEEE)


def sub(val1, val2):  # subtraction is the same as addition, (x-y) = (x+(-y))
    val2 = val2 * -1
    return add(val1, val2)


# performing  multiplication of two binary numbers
def binaryMultiply(bin1, bin2):
    bin1 = bin1.strip(".")
    bin2 = bin2.strip(".")
    binList1 = [int(x) for x in bin1]
    binList2 = [int(x) for x in bin2]
    product = []
    for i in range(1, len(binList2) + 1):
        if binList2[-i] == 1:
            arr = [x for x in binList1]
            extraZero = [0] * (i - 1)
            arr.extend(extraZero)
            product.append(arr)
    maxLen = len(product[-1])
    for i in range(len(product)):
        while len(product[i]) != maxLen:
            product[i] = [0] + product[i]
    for i in range(len(product)):
        product[i] = "".join(str(e) for e in product[i])
    while len(product) > 1:
        maxLen = max([len(x) for x in product])
        val1 = product[0]
        val2 = product[1]
        while len(val1) < maxLen:
            val1 = '0' + val1
        while len(val2) < maxLen:
            val2 = '0' + val2
        val3 = binaryAdd(val1, val2)
        product.append(val3)
        product = product[2:]
    return product[0]


def mul(val1, val2):
    if abs(val2) > abs(val1):
        val1, val2 = val2, val1
    if val1 == 0 or val2 == 0:
        return 0
    multiplier = anyfloat.from_float(val1)
    multiplierSign, multiplierExpo = multiplier.sign, multiplier.exponent
    multiplierMantissaBin = multiplier.bin(size=(11, 52)).split(" ")[2]
    multiplicand = anyfloat.from_float(val2)
    multiplicandSign = multiplicand.sign
    multiplicandExpo = multiplicand.exponent
    multiplicandMantissaBin = multiplicand.bin(size=(11, 52)).split(" ")[2]
    productSign = multiplierSign ^ multiplicandSign  # xor
    productExponent = multiplierExpo + multiplicandExpo
    allignMultiplierMant = "1" + multiplierMantissaBin
    allignMultiplicMant = '1' + multiplicandMantissaBin
    productMantissa = binaryMultiply(allignMultiplierMant, allignMultiplicMant)
    productMantissa = productMantissa[0]+'.'+productMantissa[1:-1]
    productExponent += (len(productMantissa) - 105)
    IEEE = str(productSign)+" "+bin(productExponent)+" "+productMantissa[2:]
    returnVal = convertFromIEE(IEEE)
    return returnVal


def div(val1, val2):
    """There is a faster way to do division.  Its called
   division by reciprocal approximation.  It takes about the same
   time as a fl. pt. multiply.  """
    if val2 == 0.0:
        raise DivisionZero()
    else:
        return mul(val1, 1 / val2)
