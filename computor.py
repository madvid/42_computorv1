# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys

# -- Local modules
from parsing import parser
from conversion import convert_expression
from developpement import developpement
from constants import b_bonus

# -- Specific for the handle of the bonus
if b_bonus:
	from polynomial_bonus import MyMonomial
	from polynomial_bonus import PolynomialBonus as Polynom
else:
	from polynomial import MyMonomial
	from polynomial import Polynomial as Polynom

# =========================================================================== #
# ___________________________    |FUNCTIONS|     ____________________________ #
# =========================================================================== #

def process(lst_expr:list):
	""" Converts the raw tokens into a developped polynomial instance.
	Parameter:
	----------
		* lst_expr [list of Tokens]: raw list of Tokens.
	Return:
	-------
		polynom [Polynomial object]: developped form of the polynomial.
	"""
	lst_conv = convert_expression(lst_expr)
	lst_dev = developpement(lst_conv)
	polynom = lst_dev[0]
	return polynom


def simple_graph(polynom):
	""" Plots the polynomial.
	Parameter:
	----------
		* polynom [Polynomial/PolynomialBonus]: polynomial instance.
	Return:
	-------
		None.
	"""
	nb_r = len(polynom.coefs) - 1
	f = polynom.lambda_polynom()
	c_x = polynom.coefs[-2] / (nb_r * polynom.coefs[-1])
	x = np.linspace(start= -c_x - 6, stop=-c_x + 6, num=50 * (polynom.degree + 1))
	y = list(map(polynom.lambda_p, x))
	real_roots = []
	for r in polynom.roots:
		if isinstance(r, complex):
			continue
		real_roots.append(r)
	real_roots_x = np.array(real_roots)
	real_roots_y = np.zeros(real_roots_x.shape[0])
	
	sns.set_theme()
	ax = sns.lineplot(x=x, y=y)
	sns.scatterplot(x=real_roots_x, y = real_roots_y, ax=ax)
	ax.set(xlabel = "$x$", ylabel = "$P(x)$")
	ax.axhline(0, c="black", lw=0.5)
	ax.axvline(0, c="black", lw=0.5)
	plt.show()


# =========================================================================== #
# ______________________________    |MAIN|     ______________________________ #
# =========================================================================== #
if __name__ == "__main__":
	args = sys.argv
	
	# --- Parsing of arguments
	if len(args) == 1:
		print("No argument.")
		sys.exit()
	exprs = parser(args[1:])
	if exprs is None:
		sys.exit()
	
	for expr in exprs:
		# --- Processing
		poly = process(expr)

		if isinstance(poly, MyMonomial):
			poly = Polynom([poly.coefficient])
		poly.summarize()
	
		# --- Graphic representation
		if b_bonus and poly.degree > 0:
			simple_graph(poly)