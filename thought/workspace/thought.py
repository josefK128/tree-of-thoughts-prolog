import json
from thinkgpt import ThinkGPT

class Thought:
    def __init__(self, queue, state, model_name):
        self.queue = queue
        self.state = json.loads(state)
        self.llm = ThinkGPT(model_name)
        self.query = ""
        self.reply = {}

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
