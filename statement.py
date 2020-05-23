from lang_types import *
import abc

class PrintStatement():
    def __init__(self,expression_to_print):
        self.expression_to_print = expression_to_print
    def evaluate(self,state,space_path):
        print(self.expression_to_print.evaluate(state,space_path))
        
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
        if Bool(True).EQUALS(self.condition.evaluate(state,subpath)).value ==True:
            for statement in self.if_true_statements:
                statement.evaluate(state,subpath)
        elif self.else_statements != None:
            for statement in self.else_statements:
                statement.evaluate(state,subpath)
        state.remove_namespace(subpath)
        
class UntilStatement():
    def __init__(self,condition,statements):
        self.condition = condition
        self.statements = sattements
    def evaluate(self,state,space_path):
        subpath = space_path + ['until']
        state.create_namespace(subpath)
        while Bool(False).EQUALS(self.condition.evaluate(state,subpath)).value ==True:
            for statement in self.statements:
                statement.evaluate(state,subpath)
        state.remove_namespace(subpath)
        
class NameReference():
    def __init__(self,name):
        self.name = name
    def evaluate(self,state,space_path):
        return state.get_variable(self.name,space_path)
        
        

            