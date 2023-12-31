import ply.lex as lex
import ply.yacc as yacc
import json
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
input_string = "player1 dice_move 3 player2 snake_move 30 to 3"

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

table = PrettyTable(['Step', 'Stack', 'Operation'])
step = 1

while True:
    # get one token from the input buffer
    token = lexer.token()
    token_type = '$end' if token is None else token.type
    token_value = '$' if token is None else token.value
    
    

    # get action for current_state and token
    action = parser.action[state_stack[-1]].get(token_type)

    if action<0:
        while action < 0:
            current_state = -action
            production = parser.productions[current_state]

            for _ in range(production.len):
                if stack:
                    stack.pop()
                    state_stack.pop()
                else:
                    print("Error: Stack underflow during reduction.")
                    break

            
            stack.append(production.name)
            print(stack)
            
            if state_stack:
                new_state = parsing_table[state_stack[-1]][production.name]
                print("new state : "+str(new_state))
                print("prev state : "+str(state_stack[-1]))
                print("reduced to : "+production.name)
                if new_state is not None:
                    state_stack.append(new_state)
                else:
                    print("Error: No entry in Goto table.")
                    break
            else:
                print("Error: State stack is empty after reduction.")
                break

            action = parser.action[state_stack[-1]].get(token_type)
            if action is None:
                print("Invalid token")
                break

            table.add_row([step, stack.copy(), f"Reduced to {production.name}"])
            step += 1

    if action is not None and action > 0:
        current_state = action
        state_stack.append(current_state)
        if token_value != '$':
            stack.append(token_value)
        print("Shifting to " + str(current_state))
        table.add_row([step, stack.copy(), f"Shifted to {current_state}"])
        step += 1

    elif action == 0:
        current_state = 0
        print("Accept state")
        table.add_row([step, stack.copy(), "Accept"])
        step += 1
        break
    else:
        print("Invalid token")
        table.add_row([step, stack.copy(), "Invalid token"])
        step += 1
        break
    
    print(stack)

    if isEnded:
        break

print(table)