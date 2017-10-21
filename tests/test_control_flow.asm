

                mov eax, 0
                jmp label
                dec eax
                label: inc eax

                mov eax, 0
                cmp eax, 0
                je label
                dec eax
                label: inc eax

                mov eax, 1
                cmp eax, 0
                je label
                dec eax
                label: inc eax

                mov eax, 0
                cmp eax, 0
                jne label
                dec eax
                label: inc eax
