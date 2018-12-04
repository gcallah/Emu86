# ; Declare number and sum.
# .data
#     number DW -105
#     sum DW ?
#
# ; Store first number to EAX
# ; Add 158 to value in EAX
# ; Store total to sum
# .text
#     mov eax, [number]
#     add eax, 158
#     mov [sum], eax
#
import operator as opfunc
class Sum:
    def computeSummation(value1,value2):
        return opfunc.add(value1,value2)
