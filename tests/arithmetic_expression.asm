; Declare x, y, and z variables 
.data
    x DW 35
    y DW 47
    z DW 26

; Calculate -(x + y - 2 * z + 1)
.text
    mov eax, x		
    add eax, y	
    mov ebx, z
    add ebx, ebx
    sub eax, ebx
    inc eax 
    neg eax