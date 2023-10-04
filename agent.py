# agent.py - prolog world with thoughts and actions
# thought<->world thought-reply via queue

import sys
import time
import os
import curio
from thinkgpt.llm import ThinkGPT
# Python using the swiplserver library to query prolog kb
from swiplserver import PrologMQI, PrologThread
# Tree-of-Thoughts components
import world 



# llm and tree-of-thoughts components
llm = ThinkGPT(model_name = 'gpt-3.5-turbo')

# OPENAI-API-KEY
openai_key = os.environ.get('OPENAI_API_KEY')

# history-of-thoughts
history = []

# current iteration
iterations = 0


async def prompter(queue):
    flag = True
    print(f'\n\n@@@ prompter starts: iterations set to {iterations}')
    while flag == True:
        time.sleep(2)

        # create task -
        task = world.tasks[iterations]
        world.thought['task'] = task

        # get llm response - history[1:]?
        response = llm.predict(task, remember = llm.remember(history))
        world.thought['response'] = response
 
        s = await queue.put(response)   
        print(f'\n\n@@@ prompter: sends response iterations={iterations} {response} to evaluator via queue')
        sys.stdout.flush()
        await queue.join()

        # reply
        print(f"@@@ prompter: reply = {world.thought['reply']}")


        # iteration limit
        if world.thought['reply'] == 'WIN':
            flag = False



async def evaluator(queue, prolog_filestem):
    with PrologMQI() as mqi:
        with mqi.create_thread() as prolog_thread:
            reply = prolog_thread.query(f'[{prolog_filestem}]')
            world.thought['reply'] = reply
            print(f'\n\n*** evaluator starts: consult [{prolog_filestem}] with reply={reply}')
            sys.stdout.flush()

            while world.thought['reward'] < world.thought['win']:
                response = await queue.get() 
                print(f'\n\n*** evaluator: received {response} from prompter queue')
                world.thought['response'] = response

                # reply from prolog kb
                reply = prolog_thread.query(response)
                print(f'*** evaluator: reply is {reply}') 
                world.thought['reply'] = reply

                # use rules to possibly backtrack - modify thought accordingly
                print(f'*** world.evaluate(): sets possibly new world.thought via backtrack rules')
                global iterations
                n = iterations
                n = world.evaluate(prolog_thread, n) 
                iterations = n

                # history
                print(f'*** evaluator: appends (possibly backtracked) world.thought to history')
                history.append(world.thought)
                sys.stdout.flush()
                await queue.task_done()


async def main():
    args = sys.argv[1:]
    if(len(args) != 1):
        print('commandline should be as follows:')
        print('> py agent.py prolog_filename')
        print('example> py agent.py nani.pl')
        quit() 

    # Get the file prolog_filename and extension.
    prolog_filename = args[0]
    prolog_filestem, f_ext = os.path.splitext(prolog_filename)
    print(f'prolog_filestem = {prolog_filestem}')  

    # Queue
    q = curio.Queue()

    # tasks
    evaluator_task = await curio.spawn(evaluator, q, prolog_filestem)
    prompter_task = await curio.spawn(prompter, q)
    await prompter_task.join()
    await evaluator_task.cancel()



if __name__ == '__main__':
    curio.run(main)

