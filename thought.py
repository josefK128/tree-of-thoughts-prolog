import json
from thinkgpt.llm import ThinkGPT

class Thought:
    def __init__(self, queue, axiom, index, state):
        self.queue = queue
        self.axiom = axiom
        self.index = index
        self.state = json.loads(state)
        self.llm = ThinkGPT('gpt-3.5-turbo')
        self.query = ""
        self.reply = {}   #prolog output and dynamic state
                          #{reply:str, state:Dict}

    def run:                          
        n = 0
        flag = True
        while flag == True:
            time.sleep(2)
            print(f'\nThought{self.index} sends query {axiom} to Knowledge Base')
            sys.stdout.flush()
            await queue.put(self.axiom)
            await queue.join()
            n+=1
            if n>2:
                flag = False
                print('\nThought done')
                sys.stdout.flush()

    def teach(self, prolog_syntax):
        # Teach the Thought instance Prolog query syntax
        self.query = prolog_syntax

    def get_state(self):
        # Return the current state of the Thought instance
        return json.dumps(self.state)

    def set_state(self, updated_state):
        # Update the state of the Thought instance
        self.state = json.loads(updated_state)

    def get_query(self):
        # Return the query string composed by the Thought instance
        return self.query

    def set_reply(self, reply):
        # Set the reply from the Prolog knowledge base to the Thought's query
        self.reply = json.loads(reply)
