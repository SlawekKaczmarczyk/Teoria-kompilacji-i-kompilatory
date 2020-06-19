import abc
import lang_types 
import copy


class Expression():
    @abc.abstractmethod
    def evaluate(self,state,space_path):
        pass
    
class LocalReference(Expression):
    def __init__(self, name):
        self.reference_name = name
    def evaluate(self,state,space_path):
        return state.get_variable(self.reference_name,space_path)
    def set_value(self,state,space_path,value):
#         print(f"path in local_reference {space_path}")
        path = state.get_variable_path(self.reference_name,space_path)
        
#         print(f"returned path: {path}")
        if path != None:
            state.set_variable(self.reference_name,path,value)
        
class CallVariableMethod(Expression):
    def __init__(self,expression,method_name,arguments=[]):
        self.expression = expression
        self.method_name = method_name
        self.arguments = arguments
    def evaluate(self,state,space_path):
        
        
        expression_result = self.expression.evaluate(state,space_path)
#         print(f'calling {self.method_name} on {expression_result} with args {self.arguments}')
        method = expression_result.getAttribute(self.method_name)
        lang_types.checkCallableThrow(method)
            
        return method(state,space_path,expression_result,*self.arguments)
    

    

        
    