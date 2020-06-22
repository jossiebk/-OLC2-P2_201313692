
# -----------------------------------------------------------------------------
# Jossie Bismarck Castrillo Fajardo
# 201313692
#
# Universidad de San Carlos de Guatemala
# Facultad de Ingenieria
# Escuela de Ciencias y Sistemas
# Organizacion de Lenguajes y Compiladores 2
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
#                       INICIA ANALIZADOR LEXICO
# -----------------------------------------------------------------------------
#palabras reservadas del lenguaje
reservadas = {
    'int' : 'INT',
    'char' : 'CHAR',
    'double' : 'DOUBLE',
    'float' : 'FLOAT',
    'printf' : 'PRINTF',
    'struct' : 'STRUCT',
    'if' : 'IF',
    'else' : 'ELSE',
    'switch' : 'SWITCH',
    'case' : 'CASE',
    'default' : 'DEFAULT',
    'while' : 'WHILE',
    'do' : 'DO',
    'for' : 'FOR',
    'null' : 'NULL',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'return' : 'RETURN',
    'void':'VOID'

}
# listado de tokens que manejara el lenguaje (solo la forma en la que los llamare  en las producciones)
tokens  = [
    'PUNTOYCOMA',
    'IGUAL',
    'CORCHETEDER',
    'CORCHETEIZQ',
    'PARIZQUIERDO',
    'PARDERECHO',
    'COMA',
    'LLAVEIZQ',
    'LLAVEDER',
    'PUNTO',
    'PUNTERO',
    'AMPERSAN',
    'MASIGUAL',
    'MENOSIGUAL',
    'PORIGUAL',
    'DIVIDIDOIGUAL',
    'RESIDUOIGUAL',
    'DESPLAZAMIENTOIZQ',
    'DESPLAZAMIENTODER',
    'ANDIGUAL',
    'XORIGUAL',
    'ORIGUAL',
    'NOTIGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'RESIDUO',
    'IGUALIGUAL',
    'DIFERENTE',
    'MENOR',
    'MAYOR',
    'MENORIGUAL',
    'MAYORIGUAL',
    'AND',
    'OR',
    'NOT',
    'DESPLAZAMIENTOIZQ2',
    'DESPLAZAMIENTODER2',
    'AND2',
    'OR2',
    'XOR2',
    'NOT2',
    'INCREMENTO',
    'DECREMENTO',
    'DECIMAL',
    'ENTERO',
    'ID',
    'CADENA',
    'CARACTER'
    

] + list(reservadas.values())

# Tokens y la forma en la que se usaran en el lenguaje
t_PUNTOYCOMA        = r';'
t_IGUAL             = r'='
t_CORCHETEDER = r']'
t_CORCHETEIZQ = r'\['
t_PARIZQUIERDO      = r'\('
t_PARDERECHO        = r'\)'
t_COMA =r','
t_LLAVEIZQ=r'{'
t_LLAVEDER=r'}'
t_PUNTO=r'.'
t_PUNTERO=r'->'
t_AMPERSAN=r'&'
t_MASIGUAL=r'+='
t_MENOSIGUAL=r'-='
t_PORIGUAL=r'*='
t_DIVIDIDOIGUAL=r'/='
t_RESIDUOIGUAL=r'%='
t_DESPLAZAMIENTOIZQ2=r'<<='
t_DESPLAZAMIENTODER2= r'=>>'
t_ANDIGUAL= r'&='
t_XORIGUAL= r'^='
t_ORIGUAL= r'\|='
t_INCREMENTO= r'++'
t_DECREMENTO= r'--'
t_MAS               = r'\+'
t_MENOS             = r'-'
t_POR               = r'\*'
t_DIV               = r'/'
t_RESIDUO           = r'%'
t_IGUALIGUAL        = r'=='
t_DIFERENTE         = r'!='
t_MAYORIGUAL        = r'>='
t_MENORIGUAL        = r'<='
t_MAYOR             = r'>'
t_MENOR             = r'<'
t_NOT               = r'!'
t_AND               = r'&&'
t_OR                = r'\|\|'
t_NOT2              = r'~'
t_AND2              = r'&'
t_OR2               = r'\|'
t_XOR2              = r'\^'
t_DESPLAZAMIENTOIZQ = r'<<'
t_DESPLAZAMIENTODER = r'>>'


#definife la estructura de los decimales
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("El valor decimal es muy largo %d", t.value)
        t.value = 0
    return t
#definife la estructura de los enteros
def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("El valor del entero es muy grande %d", t.value)
        t.value = 0
    return t
#definife la estructura de los identificadores que en este caso seran $letra y numero
def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
     return t
#definife la estructura de las cadenas
def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # quito las comillas del inicio y final de la cadena
    return t 

def t_CARACTER(t):
    r'\'.*?\''
    t.value = t.value[1:-1] # quito las comillas del inicio y final de la cadena
    return t 

# Comentario simple # ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1


# ----------------------- Caracteres ignorados -----------------------
# caracter equivalente a un tab
t_ignore = " \t"
#caracter equivalente a salto de linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Caracter lexico no permitido ==> '%s'" % t.value[0])
    t.lexer.skip(1)

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()


# -----------------------------------------------------------------------------
#                       INICIA ANALIZADOR SINTACTICO
# -----------------------------------------------------------------------------

# Asociación de operadores y precedencia
precedence = (
    ('left','AND','OR'),
    ('left','AND2','OR2','XOR2'),
    ('left','IGUALIGUAL','DIFERENTE'),
    ('left','MAYORIGUAL','MENORIGUAL','MAYOR','MENOR'),
    ('left','DESPLAZAMIENTOIZQ','DESPLAZAMIENTODER'),
    ('left','MAS','MENOS'),
    ('left','POR','DIV','RESIDUO'),
    ('right','UMENOS', 'NOT2','NOT'),
    )



def p_inicio(t) :
    'inicio               : inicio bloque'

def p_inicio2(t): 
    'inicio               : bloque'

def p_bloque(t):
    '''bloque:            funcoines
                        | structs
                        | instrucciones '''

def p_structs(t): 
    'structs            : STRUCT LLAVEIZQ lista_definiciones2 LLAVEDER PUNTOYDOMA'

def p_instrucciones(t):
    'instrucciones      : instrucciones instruccion'

def p_intucciones2(t):
    'instrucciones      : instruccion'

def p_instruccion(t):
    '''instruccion      : imprimir PUNTOYCOMA
                        | if_instr
                        | manejo_datos PUNTOYCOMA
                        | for_instr
                        | while_instr
                        | switch_instr
                        | BREAK PUNTOYCOMA
                        | CONTINUE PUNTOYCOMA
                        | RETURN PUNTOYCOMA
                        | RETURN expresion PUNTOYCOMA
                        |instancia PUNTOYCOMA
     '''

def p_if_instr(t):
    'if_instr           : IF PARIZQUIERDO expresion PARDERECHO LLAVEIZQ instrucciones LLAVEDER'

def p_if_instr2(t):
    'if_instr           : IF PARIZQUIERDO expresion PARDERECHO LLAVEIZQ instrucciones LLAVEDER ELSE LLAVEIZQ instrucciones LLAVEDER'

def p_if_instr3(t):
    'if_instr           : IF PARIZQUIERDO expresion PARDERECHO LLAVEIZQ instrucciones LLAVEDER ELSE if_instr'


def p_while_instr(t):
    'while_instr        : WHILE PARIZQUIERDO expresion PARDERECHO LLAVEIZQ instrucciones LLAVEDER'

def p_while_instr2(t):
    'while_instr        : DO LLAVEIZQ instrucciones LLAVEDER WHILE PARIZQUIERDO expresion PARDERECHO'

def p_switch_instr(t):
    'switch_intr        : SWITCH PARIZQUIERDO expresion PARDERECHO LLAVEIZQ casos estandar LLAVEDER'

def p_casos(t):
    'casos          : casos caso'

def p_casos2(t):
    'casos          :caso'

def p_caso(t):
    'caso           : CASE expresion DOSPUNTOS instrucciones'

def p_estandar(t):
    'estandar           : DEFAULT DOSPUNTOS instrucciones'


def for_instr(t):
    'for_instr          : FOR PARIZQUIERDO manejo_datos PUNTOYCOMA expresion PUNTOYCOMA aumento PARDERECHO LLAVEIZQ instrucciones LLAVEDER'

def p_aumento(t):
    '''aumento            : ID INCREMENTO
                          | ID DECREMENTO'''

def p_manejo_datos(t):
    '''manejo_datos         : tipo definicion'''

def p_manejo_datos2(t):
    '''manejo_datos        : asignacion '''
        
def p_lista_definiciones2(t):
    'lista_definiciones2        : lista_definiciones2 definicion'

def p_lista_definiciones3(t):
    'lista_definiciones2        : definicion'


def p_definicion(t):
    'definicion         : definicion COMA lista_definiciones'

def p_definicion2(t):
    'definicion         : lista_definiciones'

def p_lista_definiciones(t):



def p_tipo(t):
    '''tipo             : INT
                        | CHAR
                        | DOUBLE
                        | FLOAT
                        | VOID'''






#para manejar los errores sintacticos
def p_error(t): #en modo panico :v
    print("token error: ",t)
    print("Error sintáctico en '%s'" % t)

#def p_error(t): #en modo panico :v
#   while True:
#        tok=parser.token()
#        if not tok or tok.type==';':break
#    parser.errok()
#    return tok



import ply.yacc as yacc
parser = yacc.yacc()

def parse(input) :
    return parser.parse(input)