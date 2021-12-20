# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #

# =========================================================================== #
# _____________________   |Definition des constantes|   _____________________ #
# =========================================================================== #
from constants import dct_tokens, dct_precedence

# =========================================================================== #
# __________________   |Definition des classes pour AST|   __________________ #
# =========================================================================== #

class Token():
	def __init__(self, t, grp=0):
		self.value = t
		self.group = grp
		self.precedence = 0
		if t in list("()+-*/=^ˆ"):
			self.type_token = dct_tokens[t]
			self.precedence = dct_precedence[t]
		elif t.isdigit():
			self.type_token = dct_tokens["NUMBER"]
			self.value = int(t)
		elif isfloat(t):
			self.type_token = dct_tokens["NUMBER"]
			self.value = float(t)
		elif t.isalpha():
			self.type_token = dct_tokens["VARIABLE"]
			self.value = t
		else:
			self.type_token = dct_tokens["UNKNOWN"]
			self.value = t


	def __repr__(self):
		if self.type_token <= 2:
			tk_type = "Parenthesis"
		elif self.type_token <= 8:
			tk_type = "Operator"
		elif self.type_token == 9:
			tk_type = "?"
		elif self.type_token == 10:
			tk_type = "Variable"
		elif self.type_token == 11:
			tk_type = "Number"
		else:
			tk_type = "ERROR"
		return str(self.value)

# =========================================================================== #
# _____________________   |Definition des fonctions |   _____________________ #
# =========================================================================== #
def isfloat(s:str) -> bool:
	""" Functions to determine if the parameter s can be represented as a float
	Parameters:
	-----------
		* s [str]: string which could be or not a float.
	Return:
	-------
		* True: s can be represented as a float.
		* False: s cannot be represented as a float.
	"""
	float_c = list(".0123456789")
	if not all([c in float_c for c in s]):
		return False
	return True


def is_operator(token:Token) -> bool:
	""" Functions to determine if the token is an operator type.
	Parameters:
	-----------
		* token [Token instance]: a Token instance.
	Return:
	-------
		* True: token is an operator.
		* False: token is not an operator.
	"""
	if isinstance(token, Token):
		if token.value in list("+-*/ˆ^"):
			return True
	return False