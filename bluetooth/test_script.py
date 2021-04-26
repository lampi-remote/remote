import sys
from subprocess import Popen, PIPE
import time

bluetooth = Popen(['node', 'central.js'], stdout=PIPE)
buffer = b''
while True:
  out = bluetooth.stdout.read(1)
  if out != b'':
    print(out)

