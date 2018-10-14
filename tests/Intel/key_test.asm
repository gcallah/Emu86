; Asking for key input
INT 22
MOV EBX, EAX
MOV ECX, 0
MOV ESI, 0

; Move input to memory location esi
; Ask for key input again
L1: MOV [ESI], EAX
MOV EAX, 0
INT 22
INC ECX
CMP EBX,EAX
INC ESI
JNE L1

; Ask for key input 
L2: MOV EAX, 0
INT 22
DEC ECX
CMP ECX, 1
JNE L2

MOV EAX, 0
INT 22
MOV EBX, EAX

; Move input to memory location esi
; Ask for key input again
L3: MOV [ESI], EAX
INC ESI
MOV EAX, 0
INT 22
CMP EBX, EAX
JNE L3
