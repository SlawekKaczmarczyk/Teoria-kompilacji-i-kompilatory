import abc

class Expression():
    @abc.abstractmethod
    def evaluate(self,state,space_path):
        pass
    
class NameReference(Expression):
    def __init__(self, name):
        self.reference_path = [name]
    def evaluate(self,state,space_path):
        return state.get_variable(name,space_path)
    
class PrintExpression(Expression):
    def __init__(self,expression_to_print):
        self.expression_to_print = expression_to_print
    def evaluate(self,state,space_path):
        print(self.expression_to_print.evaluate(state,space_path))
    
class CallMethodExpression(Expression):
    def __init__(self,method_name,call_on,arguments):
        self.method_name = method_name
        self.call_on = call_on
        self.arguments = srguments
    def evaluate(self,state,space_path):
        return getattr(self.call_on,self.method_name)(self.call_on.evaluate(state,space_path),arguments)
    
class CreateVariable(Expression):
    def __init__(self,name,value):
        self.name = name
        self.value = value
    def evaluate(self,state,space_path):
        state.create_variable(self.name,space_path,self.value.evaluate(state,space_path))
    