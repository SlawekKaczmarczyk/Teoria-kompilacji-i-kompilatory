from state import State

class Module():
    def __init__(self,blocks):
        self.state = State()
        self.name_path = ['root']
        self.blocks = blocks
        
    def grant_state(self,state,name_path):
        self.state = state
        self.name_path = name_path
        
    def evaluate(self,state = None,name_path = None):
        if state != None:
            self.state = state
        
        for block in self.blocks:
            block.evaluate(self.state,self.name_path)
        