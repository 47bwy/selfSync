# -*- encoding: utf-8 -*-
'''
@Time    :   2025/04/01 14:16:31
@Author  :   47bwy
@Desc    :   None
'''

import glob
import re
import sys
import unicodedata

pyfiles = glob.glob('*.py')
print(pyfiles)  # 输出当前目录下所有的 Python 文件


text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
datepat = re.compile(r'(\d+)/(\d+)/(\d+)')
# datepat = re.compile(r'\d+/\d+/\d+')
r = datepat.findall(text)
print(r)  # 输出： [('11', '27', '2012'), ('3', '13', '2013')]

num = re.compile('\d+')
r = num.match('\u0661\u0662\u0663')
print(r)  # 输出：<re.Match object; span=(0, 3), match='123'>

s = 'pýtĥöñ\fis\tawesome\r\n'
print(s.upper())
cmb_chrs = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
# print(cmb_chrs)
remap = {
    ord('\t') : ' ',
    ord('\f') : ' ',
    ord('\r') : None # Deleted
}
a = s.translate(remap)
b = unicodedata.normalize('NFD', a)
print(b)
print(b.translate(cmb_chrs))


def sample():
    yield 'Is '
    yield 'Chicago '
    yield 'Not '
    yield 'Chicago '

def combine(source, maxsize):
    parts = []
    size = 0
    for part in source:
        parts.append(part)
        size += len(part)
        if size > maxsize:
            yield ''.join(parts)
            parts = []
            size = 0
    yield ''.join(parts)


for part in combine(sample(), 32768):
    print(part)

class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()


root = Node(0)
child1 = Node(1)
child2 = Node(2)
child3 = Node(3)
root.add_child(child1)
root.add_child(child2)
child1.add_child(child3)
child1.add_child(Node(4))
child2.add_child(Node(5))
child3.add_child(Node(6))

for ch in root.depth_first():
    print(ch)

# for ch in root:
#     print(ch) 

class Countdown:
    def __init__(self, start):
        self.start = start

    # Forward iterator
    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1

    # Reverse iterator
    def __reversed__(self):
        n = 1
        while n <= self.start:
            yield n
            n += 1

for rr in reversed(Countdown(30)):
    print(rr)
for rr in Countdown(30):
    print(rr)

data = [ (1, 2), (3, 4), (5, 6), (7, 8) ]
for n, (x, y) in enumerate(data):
    print(n, x, y)


import os.path


def read_into_buffer(filename):
    buf = bytearray(os.path.getsize(filename))
    with open(filename, 'rb') as f:
        f.readinto(buf)
    return buf

with open('sample.bin', 'wb') as f:
    f.write(b'Hello World')

buf = read_into_buffer('sample.bin')
print(buf)
buf[0:5] = b'HELLO'
print(buf)
m1 = memoryview(buf)
print(m1.tolist())
m2 = m1[0:5]
print(m2.tolist())

import glob
from fnmatch import fnmatch