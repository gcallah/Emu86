;;; SIEVE.ASM-Program to compute numbers of prime <= 520000
;;; using the sieve of Eratosthenes and 80386+ bit
;;; instructions
INCLUE PCMAC.INC
    .MODEL SMALL
    .586
    .STACK 100h

.data
msg1 db 'The number of prime less than $'
msg2 db ' is $'
msg3 db 13, 10, '$'

N EQU 520000;
Primes DD 0AAAAAAA8h, (N/32 - 1) DUP (0AAAAAAAAh)
;         0, 1 and multiples of 2 already crossed out

CURPRIME EQU edx
MULTIPLES EQU ebx
PrimeCount EQU edi

.code
sieve proc
EXTRN PutDDec : NEAR
      _Begin
      sub esi, esi
      mov cx, N/32 ;  Number of DWORDs to process
      mov PrimeCount, 1 ;  prime '2' already counted

ProcessDWords: ; We don't really need two labels
FindNextPrime:
    bsf eax, [Primes + 4 * esi]
    jz NextDWord ; No more primes here
    inc PrimeCount ; Count Prime


; cross out multiples

    mov CURPRIME, esi ; Compute CURPRIME
    shl CURPRIME, 5 ; = esi * 32
    add CURPRIME, eax ; + eax
    mov MULTIPLES, CURPRIME ; first cross out current prime
    shl CURPRIME, 1 ; Need only cross out odd multiples

CrossOffMultiples:
    btr Primes, MULTIPLES ; zero a multiple
    add MULTIPLES, CURPRIME
    cmp MULTIPLES, N
    j1 CrossOffMultiples
    jmp FindNextPrime

NextDWord:
    inc esi
    dec cx
    jnz ProcessDWords

    _PutStr Msg1
    mov eax, N
    call PutDDec
    _PutStr Msg2
    mov eax, PrimeCount
    call PutDDec
    _PutStr Msg3
    _Exit 0

Sieve ENDP
    END Sieve