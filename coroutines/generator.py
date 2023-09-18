# generator.py
# simple controller-generator 


import time
import sys


def controller():
  k = 0
  flag = True
  while(flag == True):
    time.sleep(2)
    yield k
    k+=1
    if(k>5):
      flag = False
      yield 'done'
#    else:
#      time.sleep(2)


def main():
  c = controller()
  print(f'\nmain waiting for controller...')
  sys.stdout.flush()
  s = next(c)
  while(s != 'done'):
    print(f'\nmain received {s} from controller')
    sys.stdout.flush()
    s = next(c)
  print(f'\nmain received {s} from controller - main exiting...')


if __name__ == "__main__":
  try:
    main()
  except OSError as e:
    print(f'error e = {e.code}')

