# simple.py
# simple async-await using curio module


import curio
import time
import sys


def controller(a):
  print(f'controller received {a}')
  sys.stdout.flush()
  k = yield a


async def main(k):
  c = controller(k)
  print(f'\nmain sending {k}')
  #c.send(k)
  sys.stdout.flush()
  s = next(c)
  print(f'main received reply {s}')
  sys.stdout.flush()


if __name__ == "__main__":
  k = 0
  while True:
    time.sleep(1)
    try:
      curio.run(main, k)
      k+=1
    except OSError as e:
      print(f'error e = {e.code}')

