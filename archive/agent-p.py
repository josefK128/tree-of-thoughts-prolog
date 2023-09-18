# agent-hToT.py


import os
from thinkgpt.llm import ThinkGPT
import openai  
import asyncio  
# Python using the swiplserver library query prolog kb
from swiplserver import PrologMQI, PrologThread
    




def main():
    print(f"PrologMQI = {PrologMQI}")
    print(f"PrologThread = {PrologThread}\n")
    
    
    # OPENAI-API-KEY
    #openai.api_key = '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'
    # Set the environment variable OPENAI_API_KEY
    os.environ['OPENAI_API_KEY'] = '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'
    value = os.environ.get('OPENAI_API_KEY')
    print("Value of OPENAI_API_KEY:", value)


    queries = ['where_am_I1(P)', 'location2(T,P)']
    with PrologMQI() as mqi:
        print(f'mqi = {mqi}')
        with mqi.create_thread() as prolog_thread:
            print(f'prolog_thread = {prolog_thread}')
            result = prolog_thread.query("consult('nani.pl')")
            print('\nconsult nani.pl done')
            result = prolog_thread.query(queries[0])
            print(f'\nquery is {queries[0]}')
            print(f'result is {result}')  
            result = prolog_thread.query(queries[1])
            print(f'\nquery is {queries[1]}')
            print(result)  
    
    
    
    # ThinkGPT    
    # get the llm
    llm = ThinkGPT(model_name="gpt-3.5-turbo")
    
    # Make the llm object learn new concepts
    llm.memorize(['DocArray is a library for representing, sending and storing multi-modal data.'])
    llm.predict('what is DocArray ?', remember=llm.remember('DocArray definition'))



if __name__ == "__main__":
    print('\n*** starting agent.py')
    #asyncio.run(main())
    main()

