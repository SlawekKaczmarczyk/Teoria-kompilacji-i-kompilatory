import abc
from expression import Expression
from state import State

class Type(Expression):
    pass

class Null(Type):
    def __init__(self): 
        self.type_name = 'NullType'
        self.value = None
    def EQUALS(self,other):
        if other.type_name == self.type_name:
            return Bool(self.value == other.value)
        else:
            return Bool(False)
    def evaluate(self,state,space_path):
        return self

class Number(Type):
    def __init__(self,number_value):
        self.type_name = 'Number'
        self.value = number_value
    def PLUS(self,other):
        if other.type_name == self.type_name:
            return Number(self.value+other.value)
    def MINUS(self,other):
        if other.type_name == self.type_name:
            return Number(self.value-other.value)
    def DIVIDE(self,other):
        if other.type_name == self.type_name:
            return Number(self.value/other.value)
    def TIMES(self,other):
        if other.type_name == self.type_name:
            return Number(self.value*other.value)
    def EQUALS(self,other):
        if other.type_name == self.type:
            return Bool(self.value == other.value)
        else:
            return Bool(False)
    def evaluate(self,state,space_path):
        return self
        
class String(Type):
    def __init__(self,string_value):
        self.type_name = 'String'
        self.value = string_value
    def PLUS(self,other):
        if other.type_name == self.type_name:
            return String(self.value+other.value)
    def EQUALS(self,other):
        if other.type_name == self.type_name:
            return Bool(self.value == other.value)
        else:
            return Bool(False)
    def evaluate(self,state,space_path):
        return self
        
class Bool(Type): 
    def __init__(self,bool_value):
        self.type_name = 'Bool'
        self.value = bool_value
    def EQUALS(self,other):
        if other.type_name == self.type_name:
            return Bool(self.value == other.value)
        else:
            return Bool(False)
    def evaluate(self,state,space_path):
        return self
        
        

    