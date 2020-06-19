from lang_types import *
from expression import * 
import abc

class PrintExpressionStatement():
    def __init__(self,expression_to_print):
        self.expression_to_print = expression_to_print
    def evaluate(self,state,space_path):
        string = CallVariableMethod(self.expression_to_print,"STR",[]).evaluate(state,space_path)
        print(string.value)
        
class ExpressionSatement():
    def __init__(self,expression):
        self.expression = expression
    def evaluate(self,state,space_path):
        self.expression.evaluate(state,space_path)
        
class IfStatement():
    def __init__(self,condition,if_true_statements,else_statements = None):
        self.condition = condition
        self.if_true_statements = if_true_statements
        self.else_statements = else_statements
        
    def evaluate(self,state,space_path):
        subpath = space_path + ['if']
        state.create_namespace(subpath)
        true = Bool(True)
        if CallVariableMethod(true,"EQUALS",[self.condition]).evaluate(state,subpath).value == True:
            for statement in self.if_true_statements:
                statement.evaluate(state,subpath)
        elif self.else_statements != None:
            for statement in self.else_statements:
                statement.evaluate(state,subpath)
        state.remove_namespace(subpath)
        
class UntilStatement():
    def __init__(self,condition,statements):
        self.condition = condition
        self.statements = statements
    def evaluate(self,state,space_path):
        subpath = space_path + ['until']
        state.create_namespace(subpath)
        true = Bool(True)
        while True:
            cond = self.condition.evaluate(state,space_path)
            print(f"cond result {cond.value}")
            condition_result = CallVariableMethod(true,"EQUALS",[cond]).evaluate(state,space_path)
            print(f"is cond true {condition_result.value}")
            if condition_result.value == False:
                for statement in self.statements:
                    statement.evaluate(state,subpath)
            else:
                break
        state.remove_namespace(subpath)
        
class VariableDefinitionStatement():
    def __init__(self,name,value):
        self.name = name
        self.value = value
    def evaluate(self,state,space_path):
        state.create_variable(self.name,space_path,self.value.evaluate(state,space_path)) 
        
class ReferenceDefinitionStatement():
    def __init__(self,ref_name,referenced_name):
        self.ref_name = ref_name
        self.referenced_name = referenced_name
    
    def evaluate(self,state,space_path):
        reference = Reference(self.referenced_name,space_path)
        state.create_variable(self.ref_name,space_path,reference)
        
class VariableSetStatement():
    def __init__(self,var_ref,expression):
        self.var_ref = var_ref
        self.expression = expression
    def evaluate(self,state,space_path):
        exp_result = self.expression.evaluate(state,space_path)
        self.var_ref.set_value(state,space_path,exp_result)
    
    
        
        

            