import ply.lex as lex
import ply.yacc as yacc
import json
from prettytable import PrettyTable


class Lexer:
    # Define tokens outside the constructor
    tokens = (
        'PLAYER',
        'DICE_MOVE',
        'SNAKE_MOVE',
        'LADDER_MOVE',
        'NUMBER',
        'TO',
    )

    # Regular expression rules for tokens
    t_PLAYER = r'player[0-9]+'
    t_DICE_MOVE = r'dice_move'
    t_SNAKE_MOVE = r'snake_move'
    t_LADDER_MOVE = r'ladder_move'
    t_NUMBER = r'[0-9]+'
    t_TO = r'to'

    # Ignored characters (whitespace)
    t_ignore = ' \t'

    def __init__(self):
        # Build the lexer
        self.lexer = lex.lex(module=self)

    # Error handling rule
    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def input(self, input_string):
        self.lexer.input(input_string)

    def token(self):
        return self.lexer.token()

class Parser:
    tokens = (
        'PLAYER',
        'DICE_MOVE',
        'SNAKE_MOVE',
        'LADDER_MOVE',
        'NUMBER',
        'TO',
    )
    def __init__(self):
        self.tokens = Parser.tokens
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self,method='SLR')
        self._build_parsing_table()

    def p_game(self, p):
        '''game : statements'''

    def p_statements(self, p):
        '''statements : statement
                      | statements statement'''

    def p_statement(self, p):
        '''statement : PLAYER move'''

    def p_move_dice(self, p):
        '''move : DICE_MOVE NUMBER'''
        if not (1 <= int(p[2]) <= 6):
            print("Dice move invalid")
            raise Exception("Invalid dice move")

    def p_move_snake(self, p):
        '''move : SNAKE_MOVE NUMBER TO NUMBER'''

    def p_move_ladder(self, p):
        '''move : LADDER_MOVE NUMBER TO NUMBER'''

    def p_error(self, p):
        print(f"Syntax error at token {p.type}")


    def _build_parsing_table(self):
        terminals_goto = self.parser.action
        non_terminals_goto = self.parser.goto
        self.parsing_table = terminals_goto
        for key,value in self.parsing_table.items():
            if non_terminals_goto.get(key) is not None:
                value.update(non_terminals_goto[key])

    def do_checks(self,input_string):
        self.parser.parse(input_string)
        
    def parse(self, input_string):
        self.lexer.input(input_string)
        stack = []
        state_stack = [0]
        current_state = 0
        isEnded = False

        table = PrettyTable(['Step', 'Stack', 'Operation'])
        table_json = {}
        step = 1

        while True:
            # get one token from the input buffer
            token = self.lexer.token()
            token_type = '$end' if token is None else token.type
            token_value = '$' if token is None else token.value
            
            # get action for current_state and token
            action = self.parsing_table[state_stack[-1]].get(token_type)

            if action<0:
                while action < 0:
                    current_state = -action
                    production = self.parser.productions[current_state]

                    for _ in range(production.len):
                        if stack:
                            stack.pop()
                            state_stack.pop()
                        else:
                            print("Error: Stack underflow during reduction.")
                            break
     
                    stack.append(production.name)
                    
                    if state_stack:
                        new_state = self.parsing_table[state_stack[-1]][production.name]
                        if new_state is not None:
                            state_stack.append(new_state)
                        else:
                            print("Error: No entry in Goto table.")
                            raise Exception("Error: No entry in Goto table.")
                    else:
                        print("Error: State stack is empty after reduction.")
                        raise Exception("Error: State stack is empty after reduction.")

                    action = self.parsing_table[state_stack[-1]].get(token_type)
                    if action is None:
                        print("Invalid token")
                        raise Exception("Invalid token")

                    table.add_row([step, stack.copy(), f"Reduced to {production.name}"])
                    table_json[step] = {'stack':stack.copy(),'operation':f"Reduced to {production.name}"}
                    step += 1

            if action is not None and action > 0:
                current_state = action
                state_stack.append(current_state)
                if token_value != '$':
                    stack.append(token_value)
                table.add_row([step, stack.copy(), f"Shifted to {current_state}"])
                table_json[step] = {'stack':stack.copy(),'operation':f"Shifted to {current_state}"}
                step += 1

            elif action == 0:
                current_state = 0
                table.add_row([step, stack.copy(), "Accept"])
                table_json[step] = {'stack':stack.copy(),'operation':"Accept"}
                step += 1
                break
            else:
                print("Invalid token")
                table.add_row([step, stack.copy(), "Invalid token"])
                table_json[step] = {'stack':stack.copy(),'operation':"Invalid token"}
                step += 1
                break

            if isEnded:
                break

        self.table_json = table_json
        print(table)

    def get_table(self):
        return self.table_json


    
if __name__ == '__main__':
    input_string = "player1 dice_move 3 player1 snake_move 30 to 10 player2 dice_move 12"
    parser = Parser()
    parser.parse(input_string)
    try:
        parser.parser.parse(input_string)
    except Exception as e:
        print(e)
    



