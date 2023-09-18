# queue-2coroutine.py - task communication via queue

import sys
import time
import curio


async def thought1(queue):
    n = 0
    flag = True
    while flag == True:
        time.sleep(2)
        print(f'\nThought1 sends query {n} to Knowledge Base')
        await queue.put(n)
        await queue.join()
        n+=1
        if n>5:
            flag = False
            print('\nThought1 done')
            sys.stdout.flush()


async def thought2(queue):
    n = 10
    flag = True
    while flag == True:
        time.sleep(2)
        print(f'\nThought2 sends query {n} to Knowledge Base')
        await queue.put(n)
        await queue.join()
        n+=1
        if n>15:
            flag = False
            print('\nThought2 done')
            sys.stdout.flush()


async def kb(queue):
    while True:
        query = await queue.get()
        if query < 10:
            print(f'\nKnowledge base recieved {query} from Thought1')
        else:
            print(f'\nKnowledge base recieved {query} from Thought2')
        sys.stdout.flush()
        await queue.task_done()


async def main():
    q = curio.Queue()
    thought1_task = await curio.spawn(thought1, q)
    thought2_task = await curio.spawn(thought2, q)
    kb_task = await curio.spawn(kb, q)
    await thought1_task.join()
    await thought2_task.join()
    await kb_task.cancel()


if __name__ == '__main__':
    curio.run(main)

