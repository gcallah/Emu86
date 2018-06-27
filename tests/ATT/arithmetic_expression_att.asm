; Declare x, y, and z variables 
.data
    x: .short 35
    y: .short 47
    z: .short 26

; Calculate -(x + y - 2 * z + 1)
.text
    mov (x), %eax		
    add (y), %eax	
    mov (z), %ebx
    add %ebx, %ebx
    sub %ebx, %eax
    inc %eax 
    neg %eax