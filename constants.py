# =========================================================================== #
# _____________________   |Definition des constantes|   _____________________ #
# =========================================================================== #
b_bonus = False

prec = 1e-6

dct_tokens = {"(" : 1,
              ")" : 2,
              "+" : 3,
              "-" : 4,
              "/" : 5,
              "*" : 6,
              "=" : 7,
              "ˆ" : 8,
              "^" : 8,
              "UNKNOWN": 9,
              "VARIABLE": 10,
              "NUMBER": 11}

dct_operator_priority = {
              "+" : 1,
              "-" : 1,
              "/" : 2,
              "*" : 2,
              "ˆ" : 3,
              '^' : 3,
              "=" : 4}

# -- precedence of the different operators
# the precedence corresponds to the operator priority.
dct_precedence = {'=' : 0,
                  '(' : 0,
                  ')' : 0,
                  '+' : 2,
                  '-' : 2,
                  '/' : 3,
                  '*' : 3,
                  'ˆ' : 4,
                  '^' : 4}

# -- dictionnary with the operators only
operators = [dct_tokens['+'],
             dct_tokens["-"],
             dct_tokens["/"],
             dct_tokens["*"],
             dct_tokens["ˆ"],
             dct_tokens['^']]


# -- operator(s) with a right/left side associativity
op_right_associativity = [dct_tokens['^'], dct_tokens["ˆ"]]
op_left_associativity = [dct_tokens['+'], dct_tokens["-"], dct_tokens["/"], dct_tokens["*"]]

# -- colors definition and font formatting constants
END = '\033[0m'
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
BLACK = "\033[1;30m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
VIOLET = "\033[1;35m"
CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
