# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
from typing import Union

# -- Local modules
from tokens import is_operator, Token
from constants import dct_tokens, b_bonus, GREEN, END

if b_bonus:
    from polynomial_bonus import MyMonomial
    from polynomial_bonus import Polynomial as Polynom
else:
    from polynomial import MyMonomial
    from polynomial import Polynomial as Polynom


# =========================================================================== #
# _____________________   |Definition des constantes|   _____________________ #
# =========================================================================== #
T_Operand = Union[MyMonomial, Polynom]

# =========================================================================== #
# _____________________   |Definition des fonctions |   _____________________ #
# =========================================================================== #

def calcul(operand_1:T_Operand, operand_2:T_Operand, operator:Token):
    """ Handles the operations between 2 Polynomial tokens, given the
    operator token.
    Parameters:
    -----------
        * operand_1 [Union[MyMonomial, Polynom]]: 1st operand.
        * operand_1 [Union[MyMonomial, Polynom]]: 2nd operand.
        * operator [Token]: the token containing the operaor to perform.
    Return:
    -------
        res [Polynomial]: result of the operation in the form of Polynomial Token.
    """
    if operator.type_token == dct_tokens['+']:
        res = operand_1 + operand_2
    elif operator.type_token ==dct_tokens['-']:
        res = operand_1 - operand_2
    elif operator.type_token ==dct_tokens['*']:
        res = operand_1 * operand_2
    elif operator.type_token ==dct_tokens['/']:
        res = operand_1 / operand_2
    elif operator.type_token in [dct_tokens["ˆ"], dct_tokens["^"]]:
        res = operand_1 ** operand_2
    return res

def developpement(lst_tkn):
    """ Performs the entire development of the expression.
    Paramters:
    ----------
        * lst_tkn [list(Mymonomial | Token)]: list of token being monomial or
                operators. The token list is in NPI form.
    Return:
    -------
        lst_tkn [list(Polynomial)]: fully developped polynomial expression.
                should be a list of only one Polynomial token.
    """
    reductible = True
    while reductible:
        ii = 0
        while (ii + 1 < len(lst_tkn)) and not is_operator(lst_tkn[ii]):
            ii += 1
        operand_1, operand_2, operator = lst_tkn[ii - 2:ii + 1]
        res = calcul(operand_1, operand_2, operator)
        del lst_tkn[ii - 2:ii+1]
        lst_tkn.insert(ii - 2, res)
        if all([not is_operator(tkn) for tkn in lst_tkn if type(tkn) == Token]):
            reductible = False
    return lst_tkn