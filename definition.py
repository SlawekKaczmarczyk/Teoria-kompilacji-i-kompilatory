


class VariableDefinition():
    def __init__(self,name,value):
        self.name = name
        self.value = value
    def evaluate(self,state,space_path):
        state.create_variable(self.name,space_path,self.value.evaluate(state,space_path)) 
        

    