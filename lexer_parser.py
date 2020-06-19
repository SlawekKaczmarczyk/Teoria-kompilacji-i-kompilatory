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
    'OPEN_PARENTHESIS',
    'CLOSE_PARENTHESIS',
    'OPEN_BRACKET',
    'CLOSE_BRACKET',
    'COLON',
    'SEMICOLON',
    'NAME',
    'EQUALS',
    'GREATER',
    'LESSER',
    'DOT',
    'COMMA',
    'STRING',
    'ASSIGN',
    'REFERENCE',
    'EOF',
    'MOD'
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
t_GREATER = r'>>'
t_LESSER = r'<<'
t_DOT = r'\.'
t_COMMA = r','
t_ASSIGN = r'<-'
t_REFERENCE = r'<='
t_MOD = r'%'


t_ignore  = ' \t'

def t_NAME(t):
    r'([a-zA-Z_])([a-zA-Z0-9_])*'
    t.type = reserved.get(t.value,'NAME')
    return t

def t_NUMBER(t):
     r'\d+'
     t.value = Number(int(t.value))   
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

precedence = (
    ('nonassoc','AND','OR'),
    ('nonassoc', 'LESSER', 'GREATER'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('left','DOT')
    
    )


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
    p[0] = PrintExpressionStatement(p[2])
    
def p_statement_2(p):
    'statement : condition SEMICOLON '
    p[0] = p[1]
    
def p_statement_3(p):
    'statement : expression SEMICOLON'
    p[0] = p[1]
    
def p_statement_4(p):
    'statement : CREATE_VAR NAME ASSIGN expression SEMICOLON'
    p[0] = VariableDefinitionStatement(p[2],p[4])
    
def p_statement_5(p):
    'statement : CREATE_VAR NAME REFERENCE NAME SEMICOLON'
    p[0] = ReferenceDefinitionStatement(p[2],p[4])
    
def p_statement_6(p):
    'statement : name_ref ASSIGN expression SEMICOLON'
    p[0] = VariableSetStatement(p[1],p[3])

def p_statement_7(p):
    'statement : FUNC_DECLARATION NAME OPEN_PARENTHESIS name_sequence CLOSE_PARENTHESIS OPEN_BRACKET function_statement_sequence CLOSE_BRACKET SEMICOLON'
    p[0] = FunctionDefinitionStatement(p[2],p[4],p[7])

def p_statement_8(p):
    'statement : FUNC_DECLARATION NAME OPEN_PARENTHESIS CLOSE_PARENTHESIS OPEN_BRACKET function_statement_sequence CLOSE_BRACKET SEMICOLON'
    p[0] = FunctionDefinitionStatement(p[2],[],p[6])
    
    
def p_statement_sequence_1(p):
    'statement_sequence : statement '
    p[0] = [p[1]]
    
def p_statement_sequence_2(p):
    'statement_sequence : statement statement_sequence '
    p[0] = [p[1]] + p[2]
    
#===========FUNCTION STATEMENT===========

def p_function_statement_1(p):
    'function_statement : statement'
    p[0] = p[1]
    
def p_fuction_satatement_2(p):
    'function_statement : RETURN expression SEMICOLON '
    p[0] = FunctionReturnStatement(p[2])
    
def p_fuction_satatement_sequence_1(p):
    'function_statement_sequence : function_statement'
    p[0] = [p[1]]
    
def p_fuction_satatement_sequence_2(p):
    'function_statement_sequence : function_statement_sequence function_statement'
    p[1].append(p[2])
    p[0] = p[1]
    
    
#===========CONDITIONS===========
    
def p_condition(p):
    """condition : if_condition
                 | until_loop"""
    p[0] = p[1]
    
def p_if_1(p):
    'if_condition : IF expression OPEN_BRACKET statement_sequence CLOSE_BRACKET'
    p[0] = IfStatement(p[2],p[4])
    
def p_if_2(p):
    'if_condition : IF  expression OPEN_BRACKET statement_sequence CLOSE_BRACKET ELSE OPEN_BRACKET statement_sequence CLOSE_BRACKET'
    p[0] = IfStatement(p[2],p[4],else_statements = p[8])
    
def p_until_loop_1(p): 
    'until_loop : UNTIL expression OPEN_BRACKET statement_sequence CLOSE_BRACKET'
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
    """expression : expression MINUS expression"""
    exp2 = CallVariableMethod(p[3],"MINUS",[])
    p[0] = CallVariableMethod(p[1],"PLUS",[exp2])

def p_expression_4(p):
    """expression : MINUS expression"""
    
    p[0] = CallVariableMethod(p[2],"MINUS",[])

# DON'T TOUCH until Number will be split to float and int

# def p_expression_4(p):
#     'expression : expression DIVIDE expression'
#     p[0] = CallVariableMethod(p[1],"DIVIDE",[p[3]])
    
def p_expression_5(p):
    'expression : expression TIMES expression'
    p[0] = CallVariableMethod(p[1],"TIMES",[p[3]])
    
def p_expression_6(p):
    'expression : expression EQUALS expression'
    p[0] = CallVariableMethod(p[1],"EQUALS",[p[3]])
    
def p_expression_7(p):
    'expression : expression LESSER expression'
    p[0] = CallVariableMethod(p[1],"LESSER",[p[3]])
    
def p_expression_8(p):
    'expression : expression GREATER expression'
    p[0] = CallVariableMethod(p[1],"GREATER",[p[3]])
    
def p_expression_9(p):
    'expression : OPEN_PARENTHESIS expression CLOSE_PARENTHESIS'
    p[0] = p[2]
    
def p_expression_10(p):
    'expression : expression DOT NAME OPEN_PARENTHESIS expression_list CLOSE_PARENTHESIS'
    p[0] = CallVariableMethod(p[1],p[3],p[5])

def p_expression_11(p):
    'expression : expression DOT NAME OPEN_PARENTHESIS CLOSE_PARENTHESIS' 
    p[0] = CallVariableMethod(p[1],p[3],[])
    
def p_expression_12(p):
    'expression : name_ref'
    p[0] = p[1]
    
def p_expression_13(p):
    'expression : name_ref OPEN_PARENTHESIS expression_list CLOSE_PARENTHESIS'
    p[0] = CallVariableMethod(p[1],"CALL",p[3])
    
def p_expression_14(p):
    'expression : name_ref OPEN_PARENTHESIS CLOSE_PARENTHESIS'
    p[0] = CallVariableMethod(p[1],"CALL",[])
    
def p_expression_15(p):
    'expression : expression AND expression'
    p[0] = CallVariableMethod(p[1],"AND",[p[3]])
    
def p_expression_16(p):
    'expression : expression OR expression'
    p[0] = CallVariableMethod(p[1],"OR",[p[3]])
    
def p_expression_17(p):
    'expression : expression MOD expression'
    p[0] = CallVariableMethod(p[1],"MOD",[p[3]])

def p_name_ref_1(p):
    'name_ref : NAME'
    p[0] = LocalReference(p[1])
    
    
#===========NAME SEQUENCE===========

def p_name_sequence_1(p):
    'name_sequence : NAME'
    p[0] = [p[1]]
    
def p_name_sequence_2(p):
    'name_sequence : NAME COMMA name_sequence '
    p[0] = [p[1]] + p[3]
    
    
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