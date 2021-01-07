Count statistics of opcodes and register / arguments in ELF binaries 

Useful tool to see some high level details and statistics of binaries. For
example, is 387 FPU used by accident on amd64 CPU, instead of SSE2? Or does the
library used AVX512 as required during compilation (sometimes some build systems
ignore user provided options / compiler flags), or see other anomalies,
interesting things.

Requires objdump and python3.

Tested with objdump from binutils 2.35.1, and Python 3.8, on Linux.

Simple use:

```
# ./elf-opcode-stats.py /bin/echo
```

# TODO

* TODO(baryluk): Statistics of register pairs.
* TODO(baryluk): Statistics of addressing modes.
* TODO(baryluk): Statistics of ngrams of opcodes maybe?
* TODO(baryluk): Opcode classification (MOV, ALU, FPU, CTRL)


# Example


`0x???` means some immediate, that was represented as 0xXYZ in the disassembly.
Remaining immediates, like 1, 4, 8, 2, 0, 3, often come from `lea`, or indexed
addressing modes.

`11111`, `1111`, `111`, `11`, means some immediete in decimal form was in
assymly, with that many decimal digits. I.e. `9123`, is converted to `1111`.
One digit ones, are left untouched.

`*0x???`, `*%rax`, etc, are indirect calls and jumps.


```
$ ./elf-opcode-stats.py /bin/ls
```

or

```
$ objdump -d /bin/ls | ./elf-opcode-stats.py
```

Output:

```
Opcode statistics:
5573 mov
1210 callq
1090 cmp
1045 je
 951 jmpq
 926 test
 889 lea
 744 xor
 737 jne
 734 pop
 596 add
 543 push
 533 nopl
 462 sub
 364 retq
 280 nopw
 269 movzbl
 239 and
 234 cmpb
 205 movb
 203 jmp
 141 movl
 130 jbe
 126 pushq
 121 movq
 101 sete
  99 ja
  97 or
  84 movslq
  80 jae
  73 data16 nopw
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
  14 movzwl
  14 cmovae
  12 fldcw
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
   5 repz cmpsb
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
   1 rep stos
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
4168 %rax
3053 1111 (1487 unique. Top: 105× 4020, 84× 41e0, 68× 40a0, 60× 46c0, 58× 49b0, 57× 4200, 51× 4220, 45× 43a0, 40× 4380, …)
1841 0x?? (67 unique. Top: 224× 0x10, 180× 0x30, 164× 0x18, 163× 0x28, 138× 0x20, 108× 0x48, 90× 0xac, 72× 0x38, 71× 0xa8, …)
1802 %rsp
1752 %eax
1519 11111 (939 unique. Top: 24× 12340, 23× 16b90, 22× 169f0, 21× 151c0, 17× 121f0, 12× 13ec9, 11× 121b7, 10× 116a0, 10× 12c78, …)
1484 %rdi
1380 %rip
1368 %rbx
1154 %rsi
1135 %rbp
1028 %rdx
 991 %edx
 963 %r12
 947 0x????? (934 unique. Top: 2× 0x20aa2, 2× 0x20a28, 2× 0x1f3e1, 2× 0x2035b, 2× 0x202f2, 2× 0x1ec6d, 2× 0x1e5a6, 2× 0x14a9a, …)
 940 $0x?? (124 unique. Top: 77× $0x20, 63× $0x30, 57× $0x10, 45× $0x2f, 39× $0x2e, 33× $0x18, 33× $0x48, 29× $0x1f, 25× $0x2b, …)
 745 1
 731 0x0
 730 %rcx
 689 $0x1
 675 %r13
 646 %edi
 545 %r14
 518 %r15
 506 $0x0
 505 %esi
 467 %al
 441 %ecx
 361 0x8
 348 %r8
 325 0x???? (317 unique. Top: 2× 0x2028, 2× 0x2038, 2× 0x1318, 2× 0x1000, 2× 0xfc24, 2× 0xfb84, 2× 0xfae4, 2× 0xfa44, 1× 0x9dde, …)
 273 $0x???? (22 unique. Top: 120× $0x4000, 96× $0xf000, 10× $0x1000, 8× $0xa000, 5× $0x2000, 4× $0x8000, 3× $0xc000, 3× $0x2520, …)
 257 %r8d
 216 $0x8
 204 %r12d
 200 %dl
 189 %r9
 182 %ebx
 168 %cs:0x0
 165 %ebp
 158 %ax
 157 $0x???????? (26 unique. Top: 86× $0xffffffff, 8× $0xfffffffd, 7× $0xffffff9c, 6× $0x7fffffff, 5× $0xfffff894, 4× $0xfffffff8, …)
 154 $0x2
 140 0x1
 124 $0x???????????????? (23 unique. Top: 69× $0xffffffffffffffff, 12× $0xfffffffffffffff8, 8× $0xffffffff92492493, 5× $0xfffffffffffffffe, …)
 119 $0x3
 115 %r13d
 112 %r9d
 111 $0x5
 110 *0x????? (110 unique. Top: 1× *0x1ffe4, 1× *0x1ffe2, 1× *0x1ffda, 1× *0x1ffd2, 1× *0x1ffca, 1× *0x1ffc2, 1× *0x1ffba, …)
 107 %fs:0x?? (1 unique. Top: 107× %fs:0x28)
 106 %r11d
 106 %xmm0
 104 $0x??? (42 unique. Top: 16× $0x400, 12× $0x100, 10× $0x200, 4× $0x118, 4× $0x2a8, 4× $0x358, 3× $0x800, 3× $0xfff, …)
 102 $0x9
  97 %r10
  97 %st
  92 %cl
  89 $0x4
  75 %r15d
  73 %xmm1
  71 %r14d
  66 %r11
  60 $0xa
  60 -0x1
  58 8
  54 4
  50 %r10d
  48 -0x??? (12 unique. Top: 20× -0x390, 9× -0x384, 8× -0x2d0, 2× -0x386, 2× -0x385, 1× -0x253, 1× -0xffa, 1× -0x2f0, 1× -0x380, …)
  45 -0x?? (17 unique. Top: 15× -0x30, 7× -0x61, 4× -0x18, 3× -0x10, 2× -0x38, 2× -0x16, 2× -0x41, 1× -0x40, 1× -0x57, …)
  39 0x??? (18 unique. Top: 5× 0x108, 4× 0x298, 4× 0x348, 3× 0x100, 3× 0x508, 3× 0x76c, 2× 0x648, 2× 0x4d0, 2× 0x286, 2× 0x4a8, …)
  37 %r12b
  35 %sil
  35 2
  34 0x2
  31 %bpl
  31 0x4
  30 %r13b
  29 %xmm2
  26 %dil
  23 $0x7
  23 $0xc
  23 %r15b
  23 0xc
  21 *%rax
  18 $0x6
  17 0
  14 -0x8
  13 %r8b
  12 0x3
  12 -0x2
  11 %bl
  11 0x9
  10 %r9b
   9 %ah
   9 *0x?? (3 unique. Top: 5× *0x30, 3× *0x38, 1× *0x40)
   8 %r14b
   8 0x7
   7 %xmm3
   7 *%rbp
   7 -0x4
   6 $0xd
   6 0xf
   6 %es:
   6 0x6
   6 *%rdx
   6 $0x??????? (3 unique. Top: 2× $0x51eb850, 2× $0x28f5c28, 2× $0x4000000)
   5 $0xb
   5 $0xe
   5 %xmm4
   5 %dx
   5 %ds:
   4 $0xf
   4 0x5
   3 $0x????? (2 unique. Top: 2× $0xfff00, 1× $0x2000e)
   2 *%rcx
   2 %r8w
   2 %xmm5
   2 %xmm6
   2 %xmm7
   2 0xb
   2 0xa
   2 3
   2 $0x??????????????? (2 unique. Top: 1× $0x800000000000000, 1× $0x400000000000000)
   2 *0x???? (2 unique. Top: 1× *0xcf2b, 1× *0xcdbb)
   1 -0x???? (1 unique. Top: 1× -0x1a24)
   1 $0x??????????? (1 unique. Top: 1× $0xffffff00000)
   1 %r10w
   1 -0x?????? (1 unique. Top: 1× -0xf0c2ac)
   1 %cx
   1 *%rbx
   1 $0x?????? (1 unique. Top: 1× $0xa3d70b)
   1 -0x6
   1 $0x????????? (1 unique. Top: 1× $0x20000002b)
   1 $0x?????????? (1 unique. Top: 1× $0x1000401001)
```
