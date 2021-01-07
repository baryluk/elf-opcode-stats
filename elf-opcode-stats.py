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
#    8016:	c3                   	retq   
#    8020:	ff 35 f2 5e 01 00    	pushq  0x15ef2(%rip)        # 1df18 <graphene_simd4x4f_transpose_in_place@@Base+0x7868>
#    8026:	ff 25 f4 5e 01 00    	jmpq   *0x15ef4(%rip)        # 1df20 <graphene_simd4x4f_transpose_in_place@@Base+0x7870>
#    802c:	0f 1f 40 00          	nopl   0x0(%rax)
#    953c:	e9 f2 fb ff ff       	jmpq   9133 <graphene_box_equal@@Base+0x1f3>
#    9541:	e8 da eb ff ff       	callq  8120 <__stack_chk_fail@plt>
#    9546:	66 2e 0f 1f 84 00 00 	nopw   %cs:0x0(%rax,%rax,1)
#    834f:	90                   	nop
#   105d8:	0f 88 a2 02 00 00    	js     10880 <__cxa_finalize@plt+0xc1b0>
#   105de:	de c9                	fmulp  %st,%st(1)
#   105e0:	f6 44 24 48 10       	testb  $0x10,0x48(%rsp)
#    fad2:	48 8d 05 c7 f6 ff ff 	lea    -0x939(%rip),%rax        # f1a0 <__cxa_finalize@plt+0xaad0>
#    fc54:	49 c7 44 24 f8 00 00 	movq   $0x0,-0x8(%r12)
#    fd26:	66 2e 0f 1f 84 00 00 	nopw   %cs:0x0(%rax,%rax,1)
#    fd56:	66 2e 0f 1f 84 00 00 	nopw   %cs:0x0(%rax,%rax,1)
#    fe63:	64 48 2b 04 25 28 00 	sub    %fs:0x28,%rax
#    fed4:	66 66 2e 0f 1f 84 00 	data16 nopw %cs:0x0(%rax,%rax,1)
#    fe8f:	00
#    fd7b:	00 00
#    fd5d:	00 00 00
#    fedb:	00 00 00 00
#   150e2:	02
#   1512d:	fd
#   1077f:	cc cc cc
#   15be4:	00 00 04
#    fab7:	00 80 3f
#    fac8:	fd b4 3f
#    ad54:	f3 48 ab             	rep stos %rax,%es:(%rdi)
#   18161:	41 ff 14 df          	callq  *(%r15,%rbx,8)
#  1cad20:	66 66 66 64 48 8b 04 	data16 data16 data16 mov %fs:0x0,%rax


line_re = re.compile(r'^ *[0-9a-f]+:\t *(?:[0-9a-f][0-9a-f] )+ *\t((?:(?:data16(?: data16)*|rep|repe|repz|repne|repnz|lock) )?[a-z0-9]+)( +[a-z0-9% \(\),\*\$:\-]*)? *(?:<[^>]+>)?(?: *|#.*)$')
assert(line_re.match('   166f8:\tc3                   \tretq'))
assert(line_re.match('   18161:	41 ff 14 df          	callq  *(%r15,%rbx,8)'))

def test_op(instruction, expected):
  m = line_re.match("   166f8:\tc3                   \t" + instruction)
  assert m, "f{instruction} didn't match opcode at all"
  assert m[1] == expected, f"test_op({instruction}) got {m[1]}, expected {expected}"
test_op('retq', 'retq')
test_op('rep stos %rax,%es:(%rdi)', 'rep stos')
test_op('lock incl (%ecx)', 'lock incl')
test_op('data16 nopw %cs:0x0(%rax,%rax,1)', 'data16 nopw')
test_op('sub ax,bx', 'sub')
test_op('cvttss2si', 'cvttss2si')
test_op('a b c', 'a')
test_op('mov ax,20', 'mov')  # ;)
test_op('jmp 0x123', 'jmp')
test_op('callq *0x123', 'callq')
test_op('data16 data16 data16 mov %fs:0x0,%rax', 'data16 data16 data16 mov')

import collections
instructions = collections.defaultdict(int)
opcodes = collections.defaultdict(int)
# This are both registers, and immediates.
# Immediates are converted to canonical form, i.e. 0xea13 is converted to 0x????
# This is to reduce the noise, and make more meaningful list, but still giving
# little bit of insight about the size of immediates.
registers = collections.defaultdict(int)
# This is list of canonical forms for immediates, mapped to a count
# of non-canonical forms, i.e. '0x????': {'0xea13': 5, '0xffff': 9, ...}
# This can be pretty big in size.
registers_full = collections.defaultdict(lambda: collections.defaultdict(int))

total_instruction_count = 0

def long_immediate_replacer(m):
  full = m.group(1)
  # We use the fact that the string is at least 2 characters.
  if full[1] == 'x':
    return '0x' + '?'*(len(m.group(1))-2)
  else:
    return '1'*len(m.group(1))

tr_table = "".maketrans("(),", "   ")

long_immediate_re = re.compile(r'(^[0-9a-f]{2,7}$|0x[0-9a-f][0-9a-f]+)')

# Non-numeric stuff is left untouched.
assert(long_immediate_re.sub(long_immediate_replacer, 'st') == 'st')
assert(long_immediate_re.sub(long_immediate_replacer, '%eax') == '%eax')

# Long ones are trimmed.
assert(long_immediate_re.sub(long_immediate_replacer, '12361233') == '12361233')
assert(long_immediate_re.sub(long_immediate_replacer, '123612') == '111111')
assert(long_immediate_re.sub(long_immediate_replacer, '123') == '111')
assert(long_immediate_re.sub(long_immediate_replacer, '42') == '11')
assert(long_immediate_re.sub(long_immediate_replacer, '0x5ef123') == '0x??????')
assert(long_immediate_re.sub(long_immediate_replacer, '0x5ef') == '0x???')
assert(long_immediate_re.sub(long_immediate_replacer, '-23') == '-23')
#assert(long_immediate_re.sub(long_immediate_replacer, '-0x21') == '-0x21')
assert(long_immediate_re.sub(long_immediate_replacer, '-0x21') == '-0x??')
#assert(long_immediate_re.sub(long_immediate_replacer, '$0x20000002b') == '$0x20000002b')
assert(long_immediate_re.sub(long_immediate_replacer, '$0x20000002b') == '$0x?????????')
#assert(long_immediate_re.sub(long_immediate_replacer, '$0x3f3f3f3f3f3f3f3f') == '$0x3f3f3f3f3f3f3f3f')
assert(long_immediate_re.sub(long_immediate_replacer, '$0x3f3f3f3f3f3f3f3f') == '$0x????????????????')
#assert(long_immediate_re.sub(long_immediate_replacer, '*0xcf2b') == '*0xcf2b')
assert(long_immediate_re.sub(long_immediate_replacer, '*0xcf2b') == '*0x????')

# Short ones are untouched.
assert(long_immediate_re.sub(long_immediate_replacer, '5') == '5')
assert(long_immediate_re.sub(long_immediate_replacer, '8') == '8')
assert(long_immediate_re.sub(long_immediate_replacer, '0') == '0')
assert(long_immediate_re.sub(long_immediate_replacer, '0x1') == '0x1')
assert(long_immediate_re.sub(long_immediate_replacer, '%cs:0x0') == '%cs:0x0')


def process_data(f):
  global opcodes, registers, total_instruction_count
  global line_re
  for line in f:
    # line = line.rstrip()
    m = line_re.match(line)
    if not m:
      # Debugging unmatched lines.
      # print(line)
      continue
    opcodes[m.group(1)] += 1
    total_instruction_count += 1

    arguments = m.group(2)
    if arguments:
      arguments = arguments.translate(tr_table)
      for register in arguments.split():
        canonical_register = long_immediate_re.sub(long_immediate_replacer, register)
        registers[canonical_register] += 1
        if canonical_register != register:
          registers_full[canonical_register][register] += 1

  # We do this outside of the main loop, as these happen
  # infrequently, and having simpler loop probably speeds
  # things up.
  # From things like "callq  *(%r15,%rbx,8)", this is because we break on (, and "*" become loose.
  if "*" in registers:
    del registers["*"]

import sys
import subprocess

if sys.argv[1:]:
  for filename in sys.argv[1:]:
    with subprocess.Popen(['objdump', '-d', filename], stdout=subprocess.PIPE, encoding='utf-8') as proc:
      process_data(proc.stdout)
else:
  process_data(sys.stdin)

# For debugging what is not captured yet by regexp.
# print(total_instruction_count)


def print_stats(d:dict, d2:dict=None):
  """Print dict(int) d, in a sorted manner, with highest ones first,
  and count column having constant width.

  Additionally, if d2 is presnet, which should be dict(dict(int)),
  check keys in it, and if present, display top values from this
  dict in a sorted manner."""
  width = None
  for k in sorted(d, key=lambda k: d[k], reverse=True):
    v = d[k]
    if not width:
      width = len(str(v))
    suffix = ""
    if d2:
      if k in d2:
        d3 = d2[k]
        top = ""
        for k3 in sorted(d3, key=lambda k3: d3[k3], reverse=True):
          if top:
            top += ", "
          if len(top) > 90:
            top += "…"
            break
          top += f"{d3[k3]}× {k3}"
        suffix += f" ({len(d3)} unique. Top: {top})"
    print(f"{v:{width}} {k}{suffix}")

# print("Instruction statistics:")
# print_stats(instructions)


print("Opcode statistics:")
print_stats(opcodes)

print()
print("Register and other opcode arguments statistics in general (source and destination):")
print_stats(registers, registers_full)
