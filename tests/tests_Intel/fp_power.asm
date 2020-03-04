; In st0, we put the number to raise to the power we put in ebx.
      fld 14.8
      mov ebx, 4
      call power
      mov eax, 0
      int 32

power: mov st1, st0
loop: fmul st0, st1
      dec ebx
      cmp ebx, 1
      jne loop
      ret
