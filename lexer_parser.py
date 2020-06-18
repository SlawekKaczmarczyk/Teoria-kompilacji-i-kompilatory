import ply.lex as lex
import ply.yacc as yacc
from lang_types import *
from expression import *
from statement import *
from definition import *
from module import *

# dokumentacja ply jest przyjemna
# 30min czytania ze zrozumieniem i wszystko wiadomo
# https://www.dabeaz.com/ply/ply.html


#===============================================
# LEXER
#===============================================
#wszystkie tokeny które będą generowane przez lexer
#

#słowa kluczowe które będą łapane przez token NAME
#zalecane są do konwertowania w funkcji t_NAME zamiast
#pisać osobny regex z powodów wydajnościowych
reserved = {
    'print' : 'PRINT',
    'var' : 'CREATE_VAR',
    'fun' : 'FUNC_DECLARATION',
    'type' : 'TYPE_DECLARATION',
    'return' : 'RETURN',
    'until' : 'UNTIL',
    'if' : 'IF',
    'else': 'ELSE',
    'and' : 'AND',
    'or' : 'OR',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'null' : 'NULL'
 }

tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'UMINUS',
    'OPEN_PARENTHESIS',
    'CLOSE_PARENTHESIS',
    'OPEN_BRACKET',
    'CLOSE_BRACKET',
    'COLON',
    'SEMICOLON',
    'NAME',
    'EQUALS',
    'DOT',
    'COMMA',
    'STRING',
    'ASSIGN',
    'EOF',
    ] + list(reserved.values())


t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_OPEN_PARENTHESIS  = r'\('
t_CLOSE_PARENTHESIS  = r'\)'
t_OPEN_BRACKET = r'\{'
t_CLOSE_BRACKET = r'\}'
t_COLON = r'\:'
t_SEMICOLON = r'\;'
t_EQUALS = r'='
t_DOT = r'\.'
t_COMMA = r','
t_ASSIGN = r'<-'


t_ignore  = ' \t'

def t_NAME(t):
    r'([a-zA-Z_])([a-zA-Z0-9_])*'
    t.type = reserved.get(t.value,'NAME')
    return t

def t_NUMBER(t):
     r'\d+'
     t.value = Number(float(t.value))   
     return t

def t_STRING(t):
    """ ".*" """
    n = len(t.value)
    if n>2 :
        t.value = String(t.value[1:n-1])
    else:
        t.value = String("")
    return t

def init_NULL(t):
    t.value = Null() 
    return t
def init_TRUE(t):
    t.value = Bool(True) 
    return t
def init_FALSE(t):
    t.value = Bool(False) 
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     raise Exception()
     t.lexer.skip(1)

lexer = lex.lex()



#===============================================
# PARSER
#===============================================
# 


def p_module(p):
    'module : block_sequence'
    p[0] = Module(p[1])

#===========BLOCK===========

def p_block_squence_1(p):
    'block_sequence : block'
    p[0] = [p[1]]
        
def p_block_squence_2(p):
    'block_sequence : block_sequence block '
    p[0] =  p[1] + [p[2]]
    
def p_block(p):
    """block : statement """
    p[0] = p[1]
    
#===========DEFINITION===========
    
# def p_definition(p):
#     """definition : variable_definition SEMICOLON"""
#     p[0] = p[1]
    


#===========STATEMENT===========

def p_statement_1(p):
    'statement : PRINT expression SEMICOLON'
    p[0] = PrintStatement(p[2])
    
def p_statement_2(p):
    'statement : condition SEMICOLON '
    p[0] = p[1]
    
def p_statement_3(p):
    'statement : expression SEMICOLON'
    p[0] = p[1]
    
def p_variable_definitions(p):
    'statement : CREATE_VAR NAME ASSIGN expression SEMICOLON'
    p[0] = VariableDefinition(p[2],p[4])
    
def p_statement_sequence_1(p):
    'statement_sequence : statement '
    p[0] = [p[1]]
    
def p_statement_sequence_2(p):
    'statement_sequence : statement statement_sequence '
    p[0] = [p[1]] + p[2]
    
#===========CONDITIONS===========
    
def p_condition(p):
    """condition : if_condition"""
    p[0] = p[1]
    
def p_if_1(p):
    'if_condition : IF expression OPEN_BRACKET statement_sequence CLOSE_BRACKET'
    p[0] = IfStatement(p[2],p[4])
    
def p_if_2(p):
    'if_condition : IF  expression OPEN_BRACKET statement_sequence CLOSE_BRACKET ELSE OPEN_BRACKET statement_sequence CLOSE_BRACKET'
    p[0] = IfStatement(p[2],p[4],else_statements = p[8])
    
def until(p): 
    'until_loop: UNTIL expression OPEN_BRACKET statement_sequence CLOSE_PARENTHESIS'
    p[0] = UntilStatement(p[2],p[4])

#===========EXPRESSION LIST===========

def p_expression_list_1(p):
    'expression_list : expression '
    p[0] = [p[1]]
    
def p_expression_list_2(p):
    'expression_list : expression_list COMMA expression'
    p[0] = p[1]
    p[0].append(p[3])
    
    
#===========EXPRESSION===========
    
def p_expression_1(p):
    'expression : value'
    p[0] = p[1]

def p_expression_2(p):
    'expression : expression PLUS expression'
    p[0] = CallVariableMethod(p[1],"PLUS",[p[3]])
    
def p_expression_3(p):
    'expression : expression MINUS expression'
    p[0] = CallVariableMethod(p[1],"MINUS",[p[3]])

def p_expression_4(p):
    'expression : expression DIVIDE expression'
    p[0] = CallVariableMethod(p[1],"DIVIDE",[p[3]])
    
def p_expression_5(p):
    'expression : expression TIMES expression'
    p[0] = CallVariableMethod(p[1],"TIMES",[p[3]])
    
def p_expression_6(p):
    'expression : OPEN_PARENTHESIS expression CLOSE_PARENTHESIS'
    p[0] = p[2]
    
def p_expression_7(p):
    'expression : expression DOT NAME OPEN_PARENTHESIS expression_list CLOSE_PARENTHESIS'
    p[0] = CallVariableMethod(p[1],p[3],p[5])
    
def p_expression_8(p):
    'expression : name_ref'
    p[0] = p[1]
    
def p_name_ref_1(p):
    'name_ref : NAME'
    p[0] = NameReference(p[1])
    
#===========VALUE===========

def p_value_from_string(p):
    'value : STRING'
    p[0] = String(p[1].value)
    
def p_value_from_number(p):
    'value : NUMBER'
    p[0] = Number(p[1].value)
    
def p_value_from_null(p):
    'value : NULL'
    p[0] = Null()
    
def p_value_from_bool(p):
    'value : bool'
    p[0] = p[1]

def p_bool(p):
    """bool : TRUE
            | FALSE"""
    if p[1] == 'true':
        p[0] = Bool(True)
    else:
        p[0] = Bool(False)
    



# Error rule for syntax errors
def p_error(p):
    print(f'Syntax error in input!\n{p}')
    t = parser.token()
    while(t != None):
        print(t)
        t = parser.token()
    raise Exception()

    
   
# Build the parser
parser = yacc.yacc()