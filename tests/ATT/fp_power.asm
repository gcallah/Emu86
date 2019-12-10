; In st0, we put the number to raise to the power we put in ebx.
      fld 14.8
      mov $4, %ebx
      call power
      mov $0, %eax
      int $32

power: mov %st0, %st1
loop: fmul %st1, %st0
      dec %ebx
      cmp %ebx, $1
      jne loop
      ret
