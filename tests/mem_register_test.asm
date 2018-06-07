; Declare arrays
.data
    x DB 1, 2, 3, 4, 5
    y DW 2, 54, 32, 8
    z DD 10 DUP (50)

; Storing values into memory using register arithmetic
; Store 6 into EAX
; Memory location 6 holds third element of x
; Memory location 8 holds fourth element of y 
; Memory location 0 holds 50
.text
	mov eax, 6
	mov [eax], x[2]
	mov [eax+2], y[3]
	mov [ebx], z