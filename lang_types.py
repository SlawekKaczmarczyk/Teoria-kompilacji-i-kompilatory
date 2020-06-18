import abc
from expression import Expression
from state import State

class Type(Expression):
    def getAttribute(self,name):
        chceckVarHasAttributeThrow(self,name)
        return self.attributes[name]

def NullEQUALS(state,space_path,*args):
    checkArgumentCountThrow(2,args)
    this = args[0]
    other = args[1].evaluate(state,space_path)
    if other.type_name == this.type_name:
        return Bool(this.value == other.value)
    else:
        return Bool(False)

class Null(Type):
    def __init__(self): 
        self.type_name = 'NullType'
        self.value = None
        self.properties = {"EQUALS" : NullEQUALS
                            }
#     def EQUALS(self,other):
#         if other.type_name == self.type_name:
#             return Bool(self.value == other.value)
#         else:
#             return Bool(False)
    def evaluate(self,state,space_path):
        return self

    
    
def NumberPLUS(state,space_path,*args):
    checkArgumentCountThrow(2,args)
    this = args[0]
    other = args[1].evaluate(state,space_path)
    checkSameTypeThrow(this,other)
    return Number(this.value+other.value)
def NumberMINUS(state,space_path,*args):
    checkArgumentCountThrow(2,args)
    this = args[0]
    other = args[1].evaluate(state,space_path)
    checkSameTypeThrow(this,other)
    return Number(this.value+other.value)
def NumberUMINUS(state,space_path,*args):
    checkArgumentCountThrow(1,args)
    this = args[0]
    return Number(-this.value)
def NumberDIVIDE(state,space_path,*args):
    checkArgumentCountThrow(2,args)
    this = args[0]
    other = args[1].evaluate(state,space_path)
    checkSameTypeThrow(this,other)
    return Number(this.value/other.value)
def NumberTIMES(state,space_path,*args):
    checkArgumentCountThrow(2,args)
    this = args[0]
    other = args[1].evaluate(state,space_path)
    checkSameTypeThrow(this,other)
    return Number(this.value*other.value)
def NumberEQUALS(state,space_path,*args):
    checkArgumentCountThrow(2,args)
    this = args[0]
    other = args[1].evaluate(state,space_path)
    checkSameTypeThrow(this,other)
    return Bool(this.value == other.value)

class Number(Type):
    def __init__(self,number_value):
        self.type_name = 'Number'
        self.value = number_value
        self.attributes = {"PLUS" : NumberPLUS,
                           "MINUS" : NumberMINUS,
                           "DIVIDE" : NumberDIVIDE,
                           "TIMES" : NumberTIMES,
                           "UMINUS": NumberUMINUS,
                           "EQUALS" : NumberEQUALS
                            }
    
#     def PLUS(self,other):
#         if other.type_name == self.type_name:
#             return Number(self.value+other.value)
#     def MINUS(self,other):
#         if other.type_name == self.type_name:
#             return Number(self.value-other.value)
#     def DIVIDE(self,other):
#         if other.type_name == self.type_name:
#             return Number(self.value/other.value)
#     def TIMES(self,other):
#         if other.type_name == self.type_name:
#             return Number(self.value*other.value)
#     def EQUALS(self,other):
#         if other.type_name == self.type:
#             return Bool(self.value == other.value)
#         else:
#             return Bool(False)
    def evaluate(self,state,space_path):
        return self
    
    
def StringPLUS(state,space_path,*args):
    checkArgumentCountThrow(2,args)
    this = args[0]
    other = args[1].evaluate(state,space_path)
    checkSameTypeThrow(this,other)
    return String(this.value + other.value)

def StringEQUALS(state,space_path,*args):
    checkArgumentCountThrow(2,args)
    this = args[0]
    other = args[1].evaluate(state,space_path)
    checkSameTypeThrow(this,other)
    return Bool(this.value == other.value)
   
        
class String(Type):
    def __init__(self,string_value):
        self.type_name = 'String'
        self.value = string_value
        self.attributes = {"PLUS" : StringPLUS,
                           "EQUALS" : StringEQUALS
                            }
#     def PLUS(self,other):
#         if other.type_name == self.type_name:
#             return String(self.value+other.value)
#     def EQUALS(self,other):
#         if other.type_name == self.type_name:
#             return Bool(self.value == other.value)
#         else:
#             return Bool(False)
    def evaluate(self,state,space_path):
        return self
        
        
        
def BoolEQUALS(state,space_path,*args):
    checkArgumentCountThrow(2,args)
    this = args[0]
    other = args[1].evaluate(state,space_path)
    checkSameTypeThrow(this,other)
    return Bool(this.value == other.value)
   
class Bool(Type): 
    def __init__(self,bool_value):
        self.type_name = 'Bool'
        self.value = bool_value
        self.attributes = {"EQUALS" : BoolEQUALS
        }
#     def EQUALS(self,other):
#         if other.type_name == self.type_name:
#             return Bool(self.value == other.value)
#         else:
#             return Bool(False)
    def evaluate(self,state,space_path):
        return self
    
class MyException(Type,Exception):
    def __init__(self,string_value):
        self.type_name = "Exception"
        self.value = string_value
        self.attributes = {}
    def evaluate(self,state,space_path):
        return self
        
        
        
        
        
        
        
        
        
def checkArgumentCountThrow(n,args):
    if len(args) != n:
        raise MyException("Wrong argument count")
        
def checkSameTypeThrow(a,b):
    if a.type_name != b.type_name:
        raise MyException("Types not matching")
        
def checkCallableThrow(x):
    if not callable(x):
        raise MyException("argument is nat callable")
        
def chceckVarHasAttributeThrow(x,attribute_name):
    if attribute_name not in x.attributes:
        raise MyException(f"argument doesn't have attribute: {attribute_name}")

        
        
        

    