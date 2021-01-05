#!/usr/bin/env python3

# Use like this:
#
#  objdump -d /bin/ls | ./elf-opcode-stats.py
#
# Opcode statistics:
# 4567 mov
#  904 test
#  801 lea
#  734 pop
#  727 xor
#  543 push
# ...
#
# Register and other opcode arguments statistics in general (source and destination):
# 3851 0x???
# 3446 %rax
# 1418 %rdi
# 1273 %eax
# 1232 %rsp
# 1209 %rbx
# 1092 %rsi
# 1018 %rbp
#  977 %rip
#  917 %r12
#...
#   4 %r9b
#   2 %xmm5
#   2 %xmm6
#   2 %xmm7
#   2 3
#   2 %dx
#   1 %r10w
#   1 %cx
#   1 %r8w


import re

# Example snippet of objdump -d
# 0000000000008020 <__acosf_finite@plt-0x10>:
#    8000:	48 83 ec 08          	sub    $0x8,%rsp
#    8004:	48 8b 05 cd 5f 01 00 	mov    0x15fcd(%rip),%rax        # 1dfd8 <__gmon_start__>
#    800b:	48 85 c0             	test   %rax,%rax
#    800e:	74 02                	je     8012 <__acosf_finite@plt-0x1e>
#    8010:	ff d0                	callq  *%rax
#    8012:	48 83 c4 08          	add    $0x8,%rsp
#    8016:	c3                   	retq...
#    8020:	ff 35 f2 5e 01 00    	pushq  0x15ef2(%rip)        # 1df18 <graphene_simd4x4f_transpose_in_place@@Base+0x7868>
#    8026:	ff 25 f4 5e 01 00    	jmpq   *0x15ef4(%rip)        # 1df20 <graphene_simd4x4f_transpose_in_place@@Base+0x7870>
#    802c:	0f 1f 40 00          	nopl   0x0(%rax)
#    953c:	e9 f2 fb ff ff       	jmpq   9133 <graphene_box_equal@@Base+0x1f3>
#    9541:	e8 da eb ff ff       	callq  8120 <__stack_chk_fail@plt>
#    9546:	66 2e 0f 1f 84 00 00 	nopw   %cs:0x0(%rax,%rax,1)
#    834f:	90                   	nop


line_re = re.compile(r'^ *[0-9a-f]+:\t *([0-9a-f][0-9a-f] )+ *\t([a-z][a-z0-9% \(\),\*\$]*) *(?: *|#.*)$')
assert(line_re.match('   166f8:\tc3                   \tretq'))

import collections
instructions = collections.defaultdict(int)
opcodes = collections.defaultdict(int)
registers = collections.defaultdict(int)

import fileinput
with fileinput.input() as f:
  for line in f:
    m = line_re.match(line.rstrip())
    if not m:
      continue
    instruction = m.group(2).strip()  # including immediates, registers, flags, etc.
    instructions[instruction] += 1
    instruction = re.sub(r'0x[0-9a-f]+', "0x???", instruction)

    arguments = re.sub(r'^[a-z0-9]+(?: +([^ ].*)|)$', r'\1', instruction)  # Strip the opcode. # The (?:  |) is to support retq, cltd, etc
    arguments = re.sub("[(),]", " ", arguments)  # We leave indirect calls and jumps, like jmpq *0x???, or callq *%rax
    for register in arguments.strip().split():
      registers[register.strip()] += 1

    # opcodes[opcode] += 1
    opcode = re.sub(" +.*", "", instruction)  # Strip arguments.  # Note. This regexp also works for retq, cltd actually.
    opcodes[opcode] += 1

#for instruction in sorted(instructions, key=lambda instruction: instructions[instruction], reverse=True):
#  print(instructions[instruction], instruction)

print("Opcode statistics:")
width = None
for opcode in sorted(opcodes, key=lambda opcode: opcodes[opcode], reverse=True):
  count = opcodes[opcode]
  if not width:
    width = len(str(count))
  print(f"{count:{width}}", opcode)


print()
print("Register and other opcode arguments statistics in general (source and destination):")
width = None
for register in sorted(registers, key=lambda register: registers[register], reverse=True):
  count = registers[register]
  if not width:
    width = len(str(count))
  print(f"{count:{width}}", register)
