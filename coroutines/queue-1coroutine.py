# queue-1coroutine.py - task communication via queue

import sys
import time
import curio


async def controller(queue):
    n = 0
    flag = True
    while flag == True:
        time.sleep(2)
        print(f'\nController sends query {n} to Knowledge Base')
        await queue.put(n)
        await queue.join()
        n+=1
        if n>5:
            flag = False
            print('\nController done')
            sys.stdout.flush()


async def kb(queue):
    while True:
        query = await queue.get()
        print(f'Knowledge base recieved {query} from Controller')
        sys.stdout.flush()
        await queue.task_done()


async def main():
    q = curio.Queue()
    controller_task = await curio.spawn(controller, q)
    kb_task = await curio.spawn(kb, q)
    await controller_task.join()
    await kb_task.cancel()


if __name__ == '__main__':
    curio.run(main)

# $ py queue-coroutine.py
# 
# Controller sends query 0 to Knowledge Base
# Knowledge base recieved 0 from Controller
# 
# Controller sends query 1 to Knowledge Base
# Knowledge base recieved 1 from Controller
# 
# Controller sends query 2 to Knowledge Base
# Knowledge base recieved 2 from Controller
# 
# Controller sends query 3 to Knowledge Base
# Knowledge base recieved 3 from Controller
# 
# Controller sends query 4 to Knowledge Base
# Knowledge base recieved 4 from Controller
# 
# Controller sends query 5 to Knowledge Base
# Knowledge base recieved 5 from Controller
#
# Controller done
