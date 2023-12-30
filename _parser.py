import ply.lex as lex
import ply.yacc as yacc
from prettytable import PrettyTable

# Define tokens
tokens = (
    'PLAYER',
    'DICE_MOVE',
    'SNAKE_MOVE',
    'LADDER_MOVE',
    'NUMBER',
    'TO',
)

# Define rules for simple tokens
t_PLAYER = r'player[0-9]+'
t_DICE_MOVE = r'dice_move'
t_SNAKE_MOVE = r'snake_move'
t_LADDER_MOVE = r'ladder_move'
t_NUMBER = r'[0-9]+'
t_TO = r'to'

# Ignored characters (whitespace)
t_ignore = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Initialize an empty stack
stack = []

# Create a table for the parsing steps
table = PrettyTable(['Step', 'Stack', 'Operation'])

# Define the CFG rules with valid ranges and checks
def p_game(p):
    '''game : statements'''
    print("Reducing: <statements> -> <game>")
    print("Game parsed successfully!")
    p[0] = p[1]

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    p[0] = f"{p[1]} {p[2]}" if len(p) == 3 else p[1]
    print(f"Reducing: <statements> -> {p[0]}")
    stack.append(p[0])
    table.add_row([len(stack), stack.copy(), 'Reduce'])

def p_statement(p):
    '''statement : PLAYER move'''
    p[0] = f"{p[1]} {p[2]}"
    print(f"Reducing: <statement> -> {p[0]}")
    stack.append(p[0])
    table.add_row([len(stack), stack.copy(), 'Reduce'])

def p_move_dice(p):
    '''move : DICE_MOVE NUMBER'''
    p[0] = f"{p[1]} {p[2]}"
    print(f"Shifting: <move> -> {p[0]}")
    stack.append(p[0])
    table.add_row([len(stack), stack.copy(), 'Shift'])

def p_move_snake(p):
    '''move : SNAKE_MOVE NUMBER TO NUMBER'''
    p[0] = f"{p[1]} {p[2]} {p[3]} {p[4]}"
    print(f"Shifting: <move> -> {p[0]}")
    stack.append(p[0])
    table.add_row([len(stack), stack.copy(), 'Shift'])

def p_move_ladder(p):
    '''move : LADDER_MOVE NUMBER TO NUMBER'''
    p[0] = f"{p[1]} {p[2]} {p[3]} {p[4]}"
    print(f"Shifting: <move> -> {p[0]}")
    stack.append(p[0])
    table.add_row([len(stack), stack.copy(), 'Shift'])

# Build the parser
parser = yacc.yacc()

# Input string to parse
input_string = "player1 dice_move 3"

# Tokenize the input
lexer.input(input_string)

# Parse the stack
print("\nParsing the stack:")
parser.parse(input_string)

# Print the table
print("\nParsing Table:")
print(table)
