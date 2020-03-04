; Asking for key input
INT $22
MOV %EAX, %EBX
MOV $0, %ECX
MOV $0, %ESI

; Move input to memory location esi
; Ask for key input again
L1: MOV %EAX, (%ESI)
MOV $0, %EAX
INT $22
INC %ECX
CMP %EAX, %EBX
INC %ESI
JNE L1

; Asking for key input
L2: MOV $0, %EAX
INT $22
DEC %ECX
CMP $1, %ECX
JNE L2

MOV $0, %EAX
INT $22
MOV %EAX, %EBX

; Move input to memory location esi
; Ask for key input again
L3: MOV %EAX, (%ESI)
INC %ESI
MOV $0, %EAX
INT $22
CMP %EAX, %EBX
JNE L3
