INT 22,0
MOV EBX,EAX
MOV ECX,0
MOV ESI,0

L1: MOV [ESI],EAX
INT 22,0
INC ECX
CMP EBX,EAX
INC ESI
JNE L1

L2: INT 22,0
DEC ECX
CMP ECX,1
JNE L2

INT 22,0
MOV EBX,EAX

L3:MOV [ESI],EAX
INC ESI
INT 22,0
CMP EBX,EAX
JNE L3