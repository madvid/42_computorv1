# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
from tokens import Token, is_operator
from constants import b_bonus

if b_bonus:
    from polynomial_bonus import MyMonomial
else:
    from polynomial import MyMonomial

# =========================================================================== #
# _____________________   |Definition des constantes|   _____________________ #
# =========================================================================== #
from constants import operators, op_left_associativity, dct_tokens

# =========================================================================== #
# __________________   |Definition des classes pour AST|   __________________ #
# =========================================================================== #

def natural_conversion(lst_tkn):
    """ This function allows to support natural expression.
    New list of tokens is created from raw list of tokens which can
    have natural expression written features, such as '2x', ')(' and so on.
    Parameters:
    -----------
        * lst_tkn [list]: list containing the raw tokens.
    Return:
    -------
        * res [list]: new list of tokens.
    """
    res = []
    prev = lst_tkn[0]
    close_after = -1

    # Dealing the 1st token explicitely: if '-', add of Token('0') before
    # To force the behavior of '-' as an substraction rather than a (-1 * )
    # operating on the next token.
    if lst_tkn[0].type_token == dct_tokens['-']:
        res = [Token('0')]
    res.append(lst_tkn[0])

    for tkn in lst_tkn[1:]:
        add_now = True
        # Handling the case where tkn('(') + tkn('0') are created
        # and the next token is '('
        if (close_after >= 0) and (tkn.type_token == dct_tokens['(']):
            close_after += 1
        if (close_after >= 0) and (tkn.type_token == dct_tokens[')']):
            close_after -= 1

        # Converting unary function of sign-change to binary operation of subtraction.
        if  tkn.type_token == dct_tokens['-'] and \
            (prev.type_token == dct_tokens['('] or is_operator(prev)):
            res += [Token('('), Token('0')]
            add_now = False
            close_after = 0
        # Handling the case of type '...)(...', '2(', '2x', and 'x2' 
        elif tkn.type_token in [dct_tokens['VARIABLE'], dct_tokens['(']] and \
           prev.type_token in [dct_tokens['VARIABLE'], dct_tokens['NUMBER'], dct_tokens[')']]:
            res.append(Token('*'))

        res.append(tkn)
        # Creating extra tkn(')') to compensate the created tkn('(')
        if add_now and close_after == 0:
            res.append(Token(')'))
            close_after = -1
        prev = tkn

    return res


def _priv_shunting_yeard_(tkn, op_stack:list):
    """ Pivate function being a part of the shunting yard algorithm
    It manages the stacking of the operators on the op_stack.
    Parameters:
    -----------
        * tkn [Token]: current token being unde consideration. To
                To decide if last token of op_stack has to be poped and
                add to output list.
        * op_stack[list(Token)]: current state of the operator stack.
              Actually we only need the last token within op_stack
    Return:
    -------
        * True/False
    """
    if len(op_stack) > 0:
        if (op_stack[-1].type_token in operators) \
            and ((op_stack[-1].precedence > tkn.precedence) \
            or (op_stack[-1].precedence == tkn.precedence) \
            and (tkn.type_token in op_left_associativity)):
            return True
        else:
            return False
    else:
        return False


def shunting_yard_algo(lst_tkn:list):
    """ Implementation of the shunting-yard algorithm.
    Parameters:
    -----------
        * lst_tkn [list]: list containing the raw tokens.
    Return:
    -------
        * lst_res [list]: list of tokens in NPI format.
    """
    output = []
    op_stack = []
    
    for tkn in lst_tkn:
        if tkn.type_token in [dct_tokens['NUMBER'], dct_tokens['VARIABLE']]:
            output.append(tkn)
        elif (tkn.type_token in operators):
            while _priv_shunting_yeard_(tkn, op_stack):
                output.append(op_stack.pop())
            op_stack.append(tkn)
        elif tkn.type_token == dct_tokens['(']:
            op_stack.append(tkn)
        elif tkn.type_token == dct_tokens[')']:
            while (len(op_stack) > 0) and (op_stack[-1].type_token != dct_tokens['(']):
                output.append(op_stack.pop())
            op_stack.pop()
    op_stack.reverse()
    for op in op_stack:
        output.append(op)
    return output


def monomial_elevation_state(lst_tkn:list):
    """
    Parameters:
    -----------
        * lst_tkn [list]: NPI tokens list.
    Return:
    -------
        * lst_res [list]: NPI tokens list where number and variable are MyMonial instances.
    """
    ii = 0
    while ii + 1 < len(lst_tkn):
        if lst_tkn[ii].type_token == dct_tokens["NUMBER"]:
            lst_tkn[ii] = MyMonomial(lst_tkn[ii].value, 0)
        elif lst_tkn[ii].type_token == dct_tokens["VARIABLE"]:
            lst_tkn[ii] = MyMonomial(1, 1)
        ii += 1
    return lst_tkn


def convert_expression(lst_tkn:list):
    """
    Parameters:
    -----------
        * lst_tkn [list]: list containing the raw tokens.
    Return:
    -------
        * lst_res [list]: NPI tokens list obtained by shunting-yeard algorithm.
    """
    lst_tkn = natural_conversion(lst_tkn)
    lst_res = shunting_yard_algo(lst_tkn)
    lst_res = monomial_elevation_state(lst_res)
    return lst_res