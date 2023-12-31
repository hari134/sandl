import ply.lex as lex
import ply.yacc as yacc
import json

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

# Define the CFG rules with valid ranges and checks
def p_game(p):
    '''game : statements'''

def p_statements(p):
    '''statements : statement
                  | statements statement'''

def p_statement(p):
    '''statement : PLAYER move'''

def p_move_dice(p):
    '''move : DICE_MOVE NUMBER'''

def p_move_snake(p):
    '''move : SNAKE_MOVE NUMBER TO NUMBER'''

def p_move_ladder(p):
    '''move : LADDER_MOVE NUMBER TO NUMBER'''

# Build the parser
parser = yacc.yacc(method='SLR')

# Input string to parse
input_string = "player1 dice_move 3 player1 snake_move 30 to 3"

# Tokenize the input
lexer.input(input_string)


parsing_table = {}
terminals_goto = parser.action
non_terminals_goto = parser.goto
parsing_table = terminals_goto

for key,value in parsing_table.items():
    if non_terminals_goto.get(key) is not None:
        value.update(non_terminals_goto[key])

print(json.dumps(parsing_table,indent=2))
for i in range(len(parser.productions)):
    print(str(i) + ' ' + parser.productions[i].str)

print(json.dumps(parsing_table,indent=2))

stack = []
state_stack = [0]
current_state = 0
isEnded = False

while True:
    # get one token from the input buffer
    token = lexer.token()
    token_type = '$end' if token is None else token.type
    token_value = '$' if token is None else token.value
    
    if token_value != '$':
        stack.append(token_value)

    # get action for current_state and token
    action = parser.action[state_stack[-1]].get(token_type)
    
    while action is not None and action < 0:
        current_state = -action
        print("Reducing to " + str(current_state))
        production = parser.productions[current_state]

        # Pop twice the length of the production to handle the recursion
        for _ in range(production.len):
            if stack:
                stack.pop()
                state_stack.pop()
            else:
                print("Error: Stack underflow during reduction.")
                break

        print(stack)
        stack.append(production.name)

        # Check if the state_stack is not empty before accessing elements
        if state_stack:
            # Update the state_stack using Goto table
            new_state = parser.goto[state_stack[-1]][production.name]
            if new_state is not None:
                state_stack.append(new_state)
            else:
                print("Error: No entry in Goto table.")
                break
        else:
            print("Error: State stack is empty after reduction.")
            break

        # Get the new action for the current state and token
        action = parser.action[state_stack[-1]].get(token_type)
        print(state_stack)

    if action is not None and action > 0:
        current_state = action
        state_stack.append(current_state)
        print("Shifting to " + str(current_state))
        print(stack)
        print(state_stack)
    elif action == 0:
        current_state = 0
        print("Accept state")
        break
    else:
        print("Invalid token")
        print(current_state)
        print(token)
        break
    
    print(stack)

    if isEnded:
        break
