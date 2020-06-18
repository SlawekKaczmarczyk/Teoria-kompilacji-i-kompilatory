import abc
import lang_types

class Expression():
    @abc.abstractmethod
    def evaluate(self,state,space_path):
        pass
    
    
class NameReference(Expression):
    def __init__(self, name):
        self.reference_name = name
    def evaluate(self,state,space_path):
        return state.get_variable(self.reference_name,space_path)
    
class PrintExpression(Expression):
    def __init__(self,expression_to_print):
        self.expression_to_print = expression_to_print
    def evaluate(self,state,space_path):
        print(self.expression_to_print.evaluate(state,space_path))
        return NullType()
    
class CreateVariable(Expression):
    def __init__(self,name,value):
        self.name = name
        self.value = value
    def evaluate(self,state,space_path):
        state.create_variable(self.name,space_path,self.value.evaluate(state,space_path))
        
# class CopyVariable(Expression):
#     def __init__(self,copy_to_name,expression):
        
        
class CallVariableMethod(Expression):
    def __init__(self,expression,method_name,arguments=[]):
        self.expression = expression
        self.method_name = method_name
        self.arguments = arguments
    def evaluate(self,state,space_path):
        expression_result = self.expression.evaluate(state,space_path)
        method = expression_result.getAttribute(self.method_name)
        lang_types.checkCallableThrow(method)
            
        return method(state,space_path,expression_result,*self.arguments)
    

        
    