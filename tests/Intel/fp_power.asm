; In F7, we put the number to raise to the power we put in F5.
      mov F7, 0x40600000
      mov F5, 0x3fb33333
      call power
      mov F4, 0x0
      int 0x20

power: mov F6, F7
loop: imul F7, F6
      dec F5
      cmp F5, 0x1
      jne loop
      ret
