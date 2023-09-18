# world-thought.py - prolog world with thought<->world query-reply via queue

import sys
import time
import curio
import os
from thinkgpt.llm import ThinkGPT
# Python using the swiplserver library to query prolog kb
from swiplserver import PrologMQI, PrologThread
#from thought import Thought

# OPENAI-API-KEY
os.environ['OPENAI_API_KEY'] = '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'
value = os.environ.get('OPENAI_API_KEY')
print("Value of OPENAI_API_KEY:", value)
sys.stdout.flush()

queries = ['where_am_I1(P)', 'location2(T,P)']

async def thought1(queue):
    n = 0
    flag = True
    while flag == True:
        time.sleep(2)
        print(f'\nThought1 sends query {queries[0]} to Knowledge Base')
        sys.stdout.flush()
        await queue.put(queries[0])
        await queue.join()
        n+=1
        if n>2:
            flag = False
            print('\nThought1 done')
            sys.stdout.flush()

async def thought2(queue):
    n = 0
    flag = True
    while flag == True:
        time.sleep(2)
        print(f'\nThought2 sends query {queries[1]} to Knowledge Base')
        sys.stdout.flush()
        await queue.put(queries[1])
        await queue.join()
        n+=1
        if n>2:
            flag = False
            print('\nThought2 done')
            sys.stdout.flush()


async def kb(queue, prolog_filestem):
    with PrologMQI() as mqi:
        with mqi.create_thread() as prolog_thread:
            #result = prolog_thread.query(f'consult({prolog_filestem})')
            result = prolog_thread.query(f'[{prolog_filestem}]')
            print(f'\nconsult {prolog_filestem} done')
            sys.stdout.flush()
            while True:
                query = await queue.get()
                print(f'\nKnowledge base recieved {query} from Thoughts')
                result = prolog_thread.query(query)
                print(f'result is {result}')  
                sys.stdout.flush()
                await queue.task_done()


async def main():
    args = sys.argv[1:]
    if(len(args) != 3):
        print('commandline should be as follows:')
        print('>py world.py prolog_filename axiom_filename evaluator_filename')
        quit() 

    # prolog kb world-specific files - <world>.pl, axiom.txt, evaluator.py 
    # Get the file prolog_filename and extension.
    prolog_filename = args[0]
    prolog_filestem, f_ext = os.path.splitext(prolog_filename)
    print(f'prolog_filestem = {prolog_filestem}')  

    # axiom_filename
    axiom_filename = args[1] 
    print(f'axiom_filename = {axiom_filename}')  
    
    # evaluator_filename
    evaluator_filename = args[2] 
    print(f'evaluator_filename = {evaluator_filename}')  


    # Queue
    q = curio.Queue()


    # Thoughts
    thought1_task = await curio.spawn(thought1, q)
    thought2_task = await curio.spawn(thought2, q)


    # kb
    kb_task = await curio.spawn(kb, q, prolog_filestem)


    # tasks
    await thought1_task.join()
    await thought2_task.join()
    await kb_task.cancel()


    # ThinkGPT    
    # get the llm
    #llm = ThinkGPT(model_name="gpt-3.5-turbo")
    
    # Make the llm object learn new concepts
    #llm.memorize(['DocArray is a library for representing, sending and storing multi-modal data.'])
    #llm.predict('what is DocArray ?', remember=llm.remember('DocArray definition'))



if __name__ == '__main__':
    curio.run(main)

