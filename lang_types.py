import abc
from expression import Expression
from state import State

class Type(Expression):
    def getAttribute(self,name):
        chceckVarHasAttributeThrow(self,name)
        return self.attributes[name]

#===========NULL===========

def NullEQUALS(state,space_path,*args):
    checkArgumentCountThrow(2,args)
    this = args[0]
    other = args[1].evaluate(state,space_path)
    if other.type_name == this.type_name:
        return Bool(this.value == other.value)
    else:
        return Bool(False)
def NullSTR(state,space_path,*args):
    checkArgumentCountThrow(1,args)
    this = args[0]
    return String("NullValue")

class Null(Type):
    def __init__(self): 
        self.type_name = 'NullType'
        self.value = None
        self.properties = {"EQUALS" : NullEQUALS,
                           "STR" : NullSTR
                            }
    def evaluate(self,state,space_path):
        return self
    
#===========REFERENCE===========

def ReferenceREF(state,space_path,*args):
    checkArgumentCountThrow(1,args)
    this = args[0]
    return state.get_variable(this.value,this.path)

def ReferenceSET(state,space_path,*args):
    checkArgumentCountThrow(2,args)
    this = args[0]
    new_val = args[1].evaluate(state,space_path)
    state.set_variable(this.value,this.path,new_val)
    return this
    
def ReferenceEQUALS(state,space_path,*args):
    checkArgumentCountThrow(2,args)
    this = args[0]
    other = args[1].evaluate(state,space_path)
    checkSameTypeThrow(this,other)
    return Bool(this.value == other.value and this.path == other.path)

def ReferenceSTR(state,space_path,*args):
    checkArgumentCountThrow(1,args)
    this = args[0]
    return String(f'Ref: {this.path}::{this.value}')
    
class Reference(Type):
    def __init__(self, name,path):
        self.value = name
        self.type_name = 'NullType'
        self.path = path
        self.attributes = {"EQUALS" : ReferenceEQUALS,
                          "SET" : ReferenceSET,
                          "REF" : ReferenceREF,
                          "STR" : ReferenceSTR}
    def evaluate(self,state,space_path):
        return self

#===========NUMBER===========
    
def NumberPLUS(state,space_path,*args):
    checkArgumentCountThrow(2,args)
    this = args[0]
    other = args[1].evaluate(state,space_path)
    checkSameTypeThrow(this,other)
    return Number(this.value+other.value)

def NumberMINUS(state,space_path,*args):
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

def NumberGREATER(state,space_path,*args):
    checkArgumentCountThrow(2,args)
    this = args[0]
    other = args[1].evaluate(state,space_path)
    checkSameTypeThrow(this,other)
    return Bool(this.value > other.value)

def NumberLESSER(state,space_path,*args):
    checkArgumentCountThrow(2,args)
    this = args[0]
    other = args[1].evaluate(state,space_path)
    checkSameTypeThrow(this,other)
    return Bool(this.value < other.value)

def NumberSTR(state,space_path,*args):
    checkArgumentCountThrow(1,args)
    this = args[0]
    return String(str(this.value))

class Number(Type):
    def __init__(self,number_value):
        self.type_name = 'Number'
        self.value = int(number_value)
        self.attributes = {"PLUS" : NumberPLUS,
                           "MINUS" : NumberMINUS,
                           "DIVIDE" : NumberDIVIDE,
                           "TIMES" : NumberTIMES,
                           "EQUALS" : NumberEQUALS,
                           "STR" : NumberSTR,
                           "GREATER" : NumberGREATER,
                           "LESSER" : NumberLESSER
                            }
    def evaluate(self,state,space_path):
        return self
    
#===========STRING===========
    
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

def StringSTR(state,space_path,*args):
    checkArgumentCountThrow(1,args)
    this = args[0]
    return String(this.value)
   
        
class String(Type):
    def __init__(self,string_value):
        self.type_name = 'String'
        self.value = string_value
        self.attributes = {"PLUS" : StringPLUS,
                           "EQUALS" : StringEQUALS,
                           "STR" : StringSTR
                            }
    def evaluate(self,state,space_path):
        return self
        
#===========BOOL===========   
        
def BoolEQUALS(state,space_path,*args):
    checkArgumentCountThrow(2,args)
    this = args[0]
    other = args[1].evaluate(state,space_path)
    checkSameTypeThrow(this,other)
    return Bool(this.value == other.value)

def BoolSTR(state,space_path,*args):
    checkArgumentCountThrow(1,args)
    this = args[0]
    if this.value == True:
        return String("true")
    else:
        return String("false")
   
class Bool(Type): 
    def __init__(self,bool_value):
        self.type_name = 'Bool'
        self.value = bool_value
        self.attributes = {"EQUALS" : BoolEQUALS,
                           "STR" : BoolSTR
        }

    def evaluate(self,state,space_path):
        return self
    
#===========BOOL===========  

def FunctionCALL(state,space_path,*args):
    this = args[0]
    checkArgumentCountThrow(1+len(this.argument_names),args)
    call_args = args[1:]
    subpath = space_path + ['fn']
    
    state.create_namespace(subpath)
    state.create_variable('return',subpath,Null())
    
    for i,name in enumerate(this.argument_names):
        state.create_variable(name,subpath,args[i+1].evaluate(state,space_path))
    
    for statement in this.body:
        statement.evaluate(state,subpath)
    
    result = state.get_variable('return',subpath)
    state.remove_namespace(subpath)
    return result
    
    
class Function(Type):
    def __init__(self,argument_names,body):
        self.argument_names = argument_names
        self.body = body
        self.attributes = {"CALL" : FunctionCALL}
    
    def evaluate(self,state,space_path):
        return self
    
    
#===========EXCEPTION===========
    
def MyExceptionSTR(state,space_path,*args):
    checkArgumentCountThrow(1,args)
    this = args[0]
    return STRING(this.value)

class MyException(Type,Exception):
    def __init__(self,string_value):
        self.type_name = "Exception"
        self.value = string_value
        self.attributes = {"STR" : MyExceptionSTR}
    def evaluate(self,state,space_path):
        return self
        
        
#===========THROW_CHCECKS===========

def checkArgumentCountThrow(n,args):
    if len(args) != n:
        raise MyException(f"Wrong argument count expected {n} got {len(args)}")
        
def checkSameTypeThrow(a,b):
    if a.type_name != b.type_name:
        raise MyException(f"Types not matching, {a.type_name} /= {b.type_name}")
        
def checkCallableThrow(x):
    if not callable(x):
        raise MyException("argument is nat callable")
        
def chceckVarHasAttributeThrow(x,attribute_name):
    if attribute_name not in x.attributes:
        raise MyException(f"argument doesn't have attribute: {attribute_name}")

        
        
        

    