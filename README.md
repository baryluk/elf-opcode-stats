Count statistics of opcodes and register / arguments in ELF binaries 

Useful tool to see some high level details and statistics of binaries. For
example, is 387 FPU used by accident on amd64 CPU, instead of SSE2? Or does the
library used AVX512 as required during compilation (sometimes some build systems
ignore user provided options / compiler flags), or see other anomalies,
interesting things.

Requires objdump and python3.

Tested with objdump from binutils 2.35.1, and Python 3.8, on Linux.


# TODO

* TODO(baryluk): Statistics of register pairs.
* TODO(baryluk): Statistics of addressing modes.
* TODO(baryluk): Statistics of ngrams of opcodes maybe?
* TODO(baryluk): Opcode classification (MOV, ALU, FPU, CTRL)
* TODO(baryluk): LOCK and REP prefixes.


# Example


`0x???` means some immediate, that was represented as 0xXYZ in the disassembly.
Remaining immediates, like 1, 4, 8, 2, 0, 3, often come from `lea`, or indexed
addressing modes.

`11111`, `1111`, `111`, `11`, means some immediete in decimal form was in
assymly, with that many decimal digits. I.e. `9123`, is converted to `1111`.
One digit ones, are left untouched.

`*0x???`, `*%rax`, etc, are indirect calls and jumps.

```
$ objdump -d /bin/ls | ./elf-opcode-stats.py

Opcode statistics:
5465 mov
1210 callq
1090 cmp
1045 je
 951 jmpq
 926 test
 801 lea
 744 xor
 737 jne
 734 pop
 596 add
 543 push
 533 nopl
 408 sub
 364 retq
 255 movzbl
 239 and
 217 cmpb
 203 jmp
 195 movb
 185 nopw
 140 movl
 130 jbe
 126 pushq
 120 movq
 101 sete
  99 ja
  97 or
  84 movslq
  80 jae
  72 xchg
  66 jg
  64 shr
  64 nop
  60 cmpq
  58 js
  48 cmpl
  45 sar
  42 cmove
  42 jl
  41 shl
  39 imul
  38 jb
  37 movups
  33 jle
  33 cmovne
  33 movdqa
  28 sbb
  28 setne
  27 div
  24 addq
  24 mul
  22 movabs
  22 testb
  22 pxor
  22 fstp
  21 jns
  18 cvtsi2ss
  17 movsbl
  17 comiss
  16 fxch
  14 cmovae
  12 fldcw
  11 movzwl
  11 not
  11 jo
  10 addss
  10 fildll
   9 seto
   9 mulss
   9 fadds
   8 movss
   7 neg
   7 fld
   7 fcomi
   7 andl
   6 andb
   6 cmovs
   6 setb
   6 seta
   6 cvttss2si
   6 btc
   6 flds
   6 fnstcw
   6 fistpll
   6 fstpt
   5 cmova
   5 ror
   5 fldt
   5 setl
   5 setge
   4 cltq
   4 cmovb
   4 orb
   4 cmovns
   4 movdqu
   4 cvtsi2sd
   4 fmul
   3 cmpw
   3 setg
   3 subss
   3 fdivrp
   3 fcomip
   3 fucomi
   3 jp
   3 fsub
   2 jge
   2 bt
   2 subq
   2 mulsd
   2 addsd
   2 movaps
   2 fmulp
   2 adc
   2 jno
   2 cmovle
   2 movsbq
   1 movw
   1 hlt
   1 setbe
   1 cmovbe
   1 shlq
   1 divq
   1 cmovge
   1 cmovl
   1 divss
   1 divsd
   1 fildl
   1 fdivp
   1 cltd
   1 idiv
   1 rol
   1 testl

Register and other opcode arguments statistics in general (source and destination):
4523 0x???
3714 $0x???
3698 %rax
3053 1111
1801 %rsp
1740 %eax
1519 11111
1458 %rdi
1375 %rip
1342 %rbx
1133 %rsi
1075 %rbp
 993 %rdx
 971 %edx
 955 %r12
 687 %rcx
 663 %r13
 639 %edi
 542 1
 539 %r14
 499 %esi
 494 %r15
 464 %al
 436 %ecx
 336 %r8
 253 %r8d
 202 %r12d
 196 %dl
 185 %r9
 182 %ebx
 165 %ebp
 156 %ax
 121 *0x???
 113 %r13d
 106 %r11d
 106 %r9d
 106 %xmm0
  97 %st
  92 %cl
  89 %r10
  74 %r15d
  73 %xmm1
  71 %r14d
  65 %r11
  54 4
  48 8
  46 %r10d
  35 2
  33 %sil
  33 %r12b
  31 %bpl
  30 %r13b
  29 %xmm2
  26 %dil
  23 %r15b
  21 *%rax
  17 0
  11 %r8b
  11 %bl
  10 %r9b
   9 %ah
   8 %r14b
   7 %xmm3
   7 *%rbp
   6 *%rdx
   5 %xmm4
   4 %dx
   2 *%rcx
   2 %r8w
   2 %xmm5
   2 %xmm6
   2 %xmm7
   2 3
   1 %r10w
   1 %cx
   1 *%rbx
   1 *
```
