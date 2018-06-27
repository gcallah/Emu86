; Declare arrays
.data
    x DB 1, 2, 3, 4, 5
    y DW 2, 54, 32, 8
    z DD 10 DUP (50)

; Storing values into memory using register arithmetic
.text
	mov eax, 6
	mov [eax], [x+2]
	mov [eax+2], [y+3]
	mov [ebx], [z]
	mov [eax-5], [y+2]