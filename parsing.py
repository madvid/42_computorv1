# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
from string import ascii_letters, digits
from tokens import Token, isfloat

# =========================================================================== #
# _____________________   |Definition des constantes|   _____________________ #
# =========================================================================== #
from constants import RED, END

# =========================================================================== #
# ____________________    |Definition des fonctions|     ____________________ #
# =========================================================================== #
def parser(argv:list):
    """ Core function of the parsing process.
    The process:
        * check length of argv (list of arguments without the python name file)
        * trims all spaces,
        * checks the presence of the symbol '=',
        * check the character composition of the expression,
    Then, tokenizes the expression (see tokenizer for more details)
    Finally, the validity of the tokenized expression is verifed (see
    check_validity for more details).
    Parameters:
    -----------
        * argv [list(str)]: list of arguments minus the program name
            when the program computor.py is executed.
    Return:
    -------
        None: if the expression(s) is/are invalid
        exprs [list(str)]: list of tokenized expressions
    """
    exprs = []
    for string in argv:
        exprs.append(string.replace(' ', ''))
    for expr in exprs:
        if check_characters(expr) is False:
            print("Invalid character(s) in one of the expression at least.")
            return None
    if all(['=' in expr for expr in exprs]):
        b_eq = True
    else:
        b_eq = False
    exprs = tokenizer(exprs)
    if any([expr is None for expr in exprs]):
        print(RED + "At least one invalid expression." + END)
        return None
    exprs = [expr for expr in exprs if len(expr) > 0]
    if not check_validity(exprs) or (b_eq == False):
        print(RED + "At least one invalid expression. (2)" + END)
        return None
    return exprs


def tokenizer(exprs:list):
    """Function tokenizes the expressions and deal with the second member
    in the expressions: moving the second member to the right side of the
    expression, changing sign when it is necessary.
    Parameters:
    -----------
        exprs [list(str)]: list of expressions to tokenize.
    Return:
    -------
        tkn_exprs [list(list(str))]: tokenized expressions.
    __Tokens: see tokens.py for full details of Token class__
    """
    tkn_exprs = []
    for expr in exprs:
        cache = []
        while len(expr) > 0:
            tkn, expr = get_token(expr)
            tkn = Token(tkn)
            cache.append(tkn)
        if any([tkn.type_token == 7 for tkn in cache]):
            cache = dealing_second_member(cache)
        tkn_exprs.append(cache)
    return tkn_exprs


def get_token(s:str):
    """ Cuts the next token from the string expression and update
    the string expression.
    Parameters:
    -----------
        * s [str]: string expression under processing.
    Return:
        * tkn [Token obj]: next token in s
        + s [str]: expression where the next token has been removed.
    """
    if s[0] in list("+-*/=^ˆ()"):
        tkn = s[0]
        s = s[1:]
        return tkn, s
    ii = 0
    if s[ii].isdigit():
        while ii < len(s) and (s[ii].isdigit() or isfloat(s[ii])):
            ii += 1
    elif s[ii].isalpha():
        while ii < len(s) and s[ii].isalpha():
            ii += 1
    tkn = s[:ii]
    s = s.lstrip(s[:ii])
    return tkn, s


def dealing_second_member(expr:list) -> list:
    """ Update the tokenized expression so that there is no second member
    expression, (similar to rearranging an expression to get 'expression = 0')
    Parameters:
    -----------
        * expr [list(str)]: tokenized expression before moving the right member
    Returns:
    --------
        * left_member [list(str)]: rearranged expression with no second member.
    """
    lst_tkn_val = [tkn.value for tkn in expr]
    try:
        nb = lst_tkn_val.count('=')
        if nb > 1:
            s_raise = "Expression with more than one '=' is invalid."
            raise Exception(s_raise)
        idx = lst_tkn_val.index('=')
        if idx + 1 == len(expr):
            return expr
        left_member = expr[:idx]
        right_member = expr[idx + 1:]
        left_member.extend(second_member_sign_update(right_member))
        return left_member
    except:
        return None



def second_member_sign_update(r_member:list) -> list:
    """ Changes the sign of the right member of the expression
    when it is necessary to take into account the displacement to the
    right side of the equal symbol.
    Prameters:
    ----------
        * r_member [list(str)]: portion of the tokenize expression
            corresponding to the right member.
    Return:
    -------
        * res [list(str)]: sign updated right member.
    """
    res = []
    lock = 0
    ii = 0
    l = len(r_member)
    while ii < l:
        tkn = r_member[ii]
        if (ii == 0) and (tkn.type_token in [10, 11]): # meaning variable or number
            res.append(Token('-'))
        if tkn.type_token == 1: # meaning value is '('
            lock += 1
        if tkn.type_token == 2: # meaning value is ')'
            lock -= 1
        if (tkn.type_token == 3) and (lock == 0): # meaning value is '+'
            tkn.value = '-'
            tkn.type_token = 4
            ii += 1
            continue
        if (tkn.type_token == 4) and (lock == 0): # meaning value is '-'
            tkn.value = '+'
            tkn.type_token = 3
            ii += 1
            continue
        ii += 1
    res.extend(r_member)
    return res


def check_characters(expr:str) -> bool:
    """ Verifies the character composition of the expression.
    Parameters:
    -----------
        * expr [str]: expression to verify.
    Return:
    -------
        * True: Expression is made of accepted characters.
        * False: Expression has non accepted characters.
    """
    valid_characters = list(ascii_letters + digits + ".+-*/=^ˆ()")
    if not all([c in valid_characters for c in expr]):
        return False
    return True


def check_validity(exprs:list) -> bool:
    """ Verifies the validity of the tokenized expression.
    More precisely:
        * verifies the the starting token: _rule_0_
        * verifies the series/order of tokens: _rule_1_
        * verifies the number of opened and closed parenthesis.
        * verifies the number variables in the expr.
    Parameters:
    -----------
        * exprs [list(list(str))]: list of all the tokenized expression.
    Return:
    -------
        * True/False [bool]: if one of the expr in exprs in invalid -> False
                             else -> True
    """
    def _rule_0_(expr:list) -> bool:
        """
        Verifies there is no invalid starting token and invalid finishing token.
        """
        tkn1, tkn2 = expr[0], expr[-1]
        if (tkn1.value in [')', '*','/','=','^', 'ˆ']) \
            or (tkn2.value in ['+','-','*','/','=','^', 'ˆ', '(']):
            return False
        return True


    def _rule_1_(expr:list) -> bool:
        """
        Verifies if succession of tokens is valid:
        2 tokens being neighbors should not be 2 operators among
        ('+','-','*','/','=','^')
        """
        ii, jj = 0, 1
        while jj < len(expr):
            tkn1, tkn2 = expr[ii], expr[jj]
            if (tkn1.value in ['+', '-', '*','/','=','^', 'ˆ']) \
                and (tkn2.value in ['+', '-', '*','/','=','^', 'ˆ']):
                return False
            ii, jj = ii+1, jj+1
        return True


    def _rule_2_(expr:list) -> bool:
        """
        Verifies the number of opened and closed parenthesis is ordered plus
        that there is '(' + ')' tokens following each other.
        """
        ii = opened = closed = 0
        prev = None
        while ii < len(expr):
            tkn = expr[ii]
            if tkn.value == '(':
                opened += 1
            if tkn.value == ')':
                closed += 1
            if closed > opened:
                return False
            if prev is not None:
                if prev.value == '(' and tkn.value == ')':
                    return False
            prev = tkn
            ii += 1
        if opened != closed:
            return False
        return True


    def _rule_3_(expr:list) -> bool:
        """
        Verifies the number variables in the expr.
        """
        n_variable = 0
        var = None
        for tkn in expr:
            if tkn.type_token == 10:
                if n_variable == 0:
                    var = tkn.value
                    n_variable = 1
                else:
                    if tkn.value != var:
                        return False
        return True
    
    for expr in exprs:
        if len(expr) < 2:
            return True
        if not _rule_0_(expr):
            return False
        if not _rule_1_(expr):
            return False
        if not _rule_2_(expr):
            return False
        if not _rule_3_(expr):
            return False
    return True