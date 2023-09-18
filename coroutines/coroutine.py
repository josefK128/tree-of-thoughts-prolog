# coroutine
# simple controller-coroutinebased on Ramalho p484-485 


import time
import sys
import random


def controller():
  total = 0.0
  count = 1
  average = 0.0
  print(f'\ncontroller initial average is {average} = {total}/{count}')
  flag = True
  while(flag == True):
    time.sleep(2)
    term = yield average
    print(f'controller received term = {term} from main')
    total+=term
    count+=1
    average = total/count
    print(f'controller average is now {average} = {total}/{count}')
    if(count>5):
      flag = False
      yield 'done'


def main():
  k = 10
  print(f'\nmain waiting for controller...')
  sys.stdout.flush()
  c = controller()
  s = next(c)
  while(s != 'done'):
    print(f'\nmain received average = {s} from controller')
    sys.stdout.flush()
    k = random.randint(1,10)
    print(f'\nmain sending new term = {k} to controller')
    s = c.send(k)
  print(f'\nmain received {s} from controller - main exiting...')


if __name__ == "__main__":
  try:
    main()
  except OSError as e:
    print(f'error e = {e.code}')

