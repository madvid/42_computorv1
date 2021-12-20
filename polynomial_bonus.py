# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
from tokens import Token
from polynomial import Polynomial, babylonian_sqrt, power, _conv_tokens_2_lst_
from constants import prec
# =========================================================================== #
# ______________________   |Definition des classes |   ______________________ #
# =========================================================================== #

class MyMonomial(Token):
    def __init__(self, coefficient, exponent):
        value = str(coefficient) + 'X^' + str(exponent)
        Token.__init__(self, value) 
        self.coefficient = coefficient
        self.exponent = exponent


    def __repr__(self):
        s_coef, s_var, s_exp = '', '', ''
        if abs(self.exponent) >= 1:
            s_var = 'X'
        if self.exponent > 1 or self.exponent <= -1:
            s_exp = '^' + str(self.exponent)
        if abs(self.coefficient) != 1 or self.exponent == 0 :
            s_coef = str(self.coefficient)
        elif self.coefficient == -1:
            s_coef = '-'
        if self.coefficient == 0:
            return '0'
        return '' + s_coef + s_var + s_exp

    def __add__(self, other):
        if isinstance(other, MyMonomial):
            if self.exponent == other.exponent:
                res = MyMonomial(self.coefficient + other.coefficient, self.exponent)
                return (res)
            else:
                res = PolynomialBonus(_conv_tokens_2_lst_(self, other))
                return res
        elif isinstance(other, PolynomialBonus):
            return other + self
        else:
            raise TypeError()

    def __radd__(self, other):
        if isinstance(other, MyMonomial):
            if  self.exponent == other.exponent:
                res = MyMonomial(other.coefficient + self.coefficient, self.exponent)
            else:
                res = PolynomialBonus(_conv_tokens_2_lst_(other, self))
            return res
        else:
            raise TypeError()

    def __sub__(self, other):
        if isinstance(other, MyMonomial):
            if self.exponent == other.exponent:
                res = MyMonomial(self.coefficient - other.coefficient, self.exponent)
            else:
                other.coefficient = - other.coefficient
                res = PolynomialBonus(_conv_tokens_2_lst_(self, other))
            return res
        elif isinstance(other, PolynomialBonus):
            other.coefs = [-c for c in other.coefs]
            return  other + self
        else:
            raise TypeError()

    def __rsub__(self, other):
        if isinstance(other, MyMonomial):
            if self.exponent == other.exponent:
                res = MyMonomial(-other.coefficient + self.coefficient, self.exponent)
            else:
                self.coefficient = - self.coefficient
                res = PolynomialBonus(_conv_tokens_2_lst_(other, self))
            return res
        else:
            raise TypeError()

    def __mul__(self, other):
        if isinstance(other, MyMonomial):
            res = MyMonomial(other.coefficient * self.coefficient, self.exponent + other.exponent)
            return res
        elif isinstance(other, PolynomialBonus):
            return other * self
        else:
            raise TypeError()

    def __rmul__(self, other):
        if isinstance(other, MyMonomial):
            res = MyMonomial(other.coefficient * self.coefficient, other.exponent + self.exponent)
            return res

    def __truediv__(self, other):
        if isinstance(other, MyMonomial):
            if other.coefficient != 0:
                res = MyMonomial(self.coefficient / other.coefficient, self.exponent - other.exponent)
                return res
            else:
                raise ZeroDivisionError()
        else:
            raise TypeError()

    def __rtruediv__(self, other):
        if isinstance(other, MyMonomial):
            if self.coefficient != 0:
                res = MyMonomial(other.coefficient / self.coefficient, other.exponent - self.exponent)
                return res
            else:
                raise ZeroDivisionError()
        else:
            raise TypeError()

    def __pow__(self, other):
        if isinstance(other, MyMonomial):
            if other.exponent == 0 and isinstance(other.coefficient, int):
                res = MyMonomial(power(self.coefficient,other.coefficient), self.exponent * other.coefficient)
                return res
            else:
                raise ValueError()
        else:
            raise TypeError()
    
    #def __rpow__(self, other):
    #	pass
class PolynomialBonus(Polynomial):
    
    def _third_degree_resolution_(self):
        """
        Calculates the roots of polynomial of degree 3.
        The method is the general cubic formulation deduced from Cardano's formula.
        (wiki source)
        Return:
        -------
            * r... [floats/complexes]: roots of the polynomial.
        """
        # reference: https://fr.wikiversity.org/wiki/Équation_du_troisième_degré/Méthode_de_Cardan
        if self.degree == 3:
            # Point important: n'est traité que le cas où les coefficients sont réels
            a = self.coefs[3]
            b = self.coefs[2]
            c = self.coefs[1]
            d = self.coefs[0]
            p = c/a - power(b, 2) / (3 * a * a)
            q = (2 * b * b * b - 9 * a * b * c + 27 * a * a * d) / (27 * a * a * a)
            delta_Cardan = - (4 * p * p * p + 27 * q * q)
            j = 0.5 * complex(-1, babylonian_sqrt(3))
            if delta_Cardan == 0:
                r0 = 3 * (q / p) - b / (3 * a)
                r1 = r2 = - 1.5 * (q / p) - b / (3 * a)
            if delta_Cardan > 0:
                u = 0.5 * complex(-q, babylonian_sqrt(delta_Cardan / 27))
                u = u ** (1/3)
                r0 = u + u.conjugate() - (b / (3 * a))
                r1 = j * u + (j * u).conjugate() - (b / (3 * a))
                r2 = j * j * u + (j * j * u).conjugate() - (b / (3 * a))
                r0 = r0.real
                r1 = r1.real
                r2 = r2.real
            if delta_Cardan < 0:
                r0 = binary_search_cubic_root(0.5 * (-q + babylonian_sqrt(-delta_Cardan/27))) \
                    + binary_search_cubic_root(0.5 * (-q - babylonian_sqrt(-delta_Cardan/27))) \
                        - b / (3 * a)
                r1 = j * binary_search_cubic_root(0.5 * (-q + babylonian_sqrt(-delta_Cardan/27))) \
                    + j * j * binary_search_cubic_root(0.5 * (-q - babylonian_sqrt(-delta_Cardan/27))) \
                        - b / (3 * a)
                r2 = j * j * binary_search_cubic_root(0.5 * (-q + babylonian_sqrt(-delta_Cardan/27))) \
                    + j * binary_search_cubic_root(0.5 * (-q - babylonian_sqrt(-delta_Cardan/27))) \
                        - b / (3 * a)
            return [r0, r1, r2]
        else:
            print("Polynomial is not of 3rd degree.")


    def _summarize_degree_3(self):
        """Displays type function.
        Function prints:
            * reduced form of the Polynomial instance.
            * natural form of the Polynomial.
            * degree of the Polynomial.
            * discriminant of the Polynomial.
            * delta0, delta1 and Cardano coefficient of the Polynomial.
            * roots of the Polynomial.
        """
        print("Reduced form:".ljust(20), self.__repr__() + "= 0")
        print("Natural form:".ljust(20), self.natural_form() + "= 0")
        print("Factorized form:".ljust(20), self.factorized_form())
        print("Polynomial degree:".ljust(20), self.degree)
        delta = self.discriminant()
        r = self._third_degree_resolution_()
        print(f"Discriminant:".ljust(20), delta)
        if delta < 0:
            print("Discriminant is strictly negative, the real root and the 2 complex roots are:")
        elif delta == 0:
            print("Discriminant is null, the roots are all real and are:")
        else:
            print("Discriminant is strictly positive, the three solutions are:")
        Polynomial._print_roots(r)

    
    def __add__(self, other):
        if isinstance(other, MyMonomial):
            if len(self.coefs) > other.exponent + 1:
                new_coefs = self.coefs
                new_coefs[other.exponent] += other.coefficient
            else:
                new_coefs = self.coefs + [0] * (other.exponent + 1 - self.degree)
                new_coefs[other.exponent] += other.coefficient
            return PolynomialBonus(new_coefs)
        if isinstance(other, PolynomialBonus):
            if self.degree >= other.degree:
                new_coefs = self.coefs
                remind = other.coefs
            else:
                new_coefs = other.coefs
                remind = self.coefs
            for ii,val in enumerate(remind):
                new_coefs[ii] += val
            return PolynomialBonus(new_coefs)
        raise TypeError()

    def __radd__(self, other):
        if isinstance(other, MyMonomial):
            if len(self.coefs) > other.exponent + 1:
                new_coefs = self.coefs
                new_coefs[other.exponent] += other.coefficient
            else:
                new_coefs = self.coefs + [0] * (other.exponent + 1 - self.degree)
                new_coefs[other.exponent] += other.coefficient
            return PolynomialBonus(new_coefs)
        if isinstance(other, PolynomialBonus):
            if self.degree >= other.degree:
                new_coefs = self.coefs
                remind = other.coefs
            else:
                new_coefs = other.coefs
                remind = self.coefs
            for ii,val in enumerate(remind):
                new_coefs[ii] += val
            return PolynomialBonus(new_coefs)
        raise TypeError()

    def __sub__(self, other):
        if isinstance(other, MyMonomial):
            if len(self.coefs) > other.exponent + 1:
                new_coefs = self.coefs
                new_coefs[other.exponent] -= other.coefficient
            else:
                new_coefs = self.coefs + [0] * (other.exponent + 1 - self.degree)
                new_coefs[other.exponent] -= other.coefficient
            return PolynomialBonus(new_coefs)
        if isinstance(other, PolynomialBonus):
            if self.degree >= other.degree:
                new_coefs = self.coefs
                remind = list(map(lambda x : -x, other.coefs))
            else:
                new_coefs = list(map(lambda x : -x, other.coefs))
                remind = self.coefs
            for ii,val in enumerate(remind):
                new_coefs[ii] += val
            return PolynomialBonus(new_coefs)
        raise TypeError()

    def __rsub__(self, other):
        if isinstance(other, MyMonomial):
            new_coefs = list(map(lambda x : -x, self.coefs))
            if len(self.coefs) > other.exponent + 1:
                new_coefs[other.exponent] += other.coefficient
            else:
                new_coefs = self.coefs + [0] * (other.exponent + 1 - self.degree)
                new_coefs[other.exponent] += other.coefficient
            return PolynomialBonus(new_coefs)
        if isinstance(other, Polynomial):
            if self.degree >= other.degree:
                new_coefs = list(map(lambda x : -x, self.coefs))
                remind = other.coefs
            else:
                new_coefs = other.coefs
                remind = list(map(lambda x : -x, self.coefs))
            for ii,val in enumerate(remind):
                new_coefs[ii] += val
            return PolynomialBonus(new_coefs)
        raise TypeError()

    def __mul__(self, other):
        if isinstance(other, MyMonomial):
            new_coefs = [c * other.coefficient for c in self.coefs]
            new_coefs = [0] * other.exponent + self.coefs
            return PolynomialBonus(new_coefs)
        elif isinstance(other, PolynomialBonus):
            new_coefs = [0] * (self.degree + other.degree + 1)
            for ii, elem in enumerate(self.coefs):
                tmp = [0] * ii + [c * elem for c in other.coefs]
                for jj in range(len(tmp)):
                    new_coefs[jj] += tmp[jj]
            return PolynomialBonus(new_coefs)
        else:
            raise TypeError()

    def __rmul__(self, other):
        if isinstance(other, MyMonomial):
            new_coefs = [c * other.coefficient for c in self.coefs]
            new_coefs = [0] * other.exponent + self.coefs
            return PolynomialBonus(new_coefs)
        elif isinstance(other, PolynomialBonus):
            new_coefs = [0] * (self.degree + other.degree + 1)
            for ii, elem in enumerate(self.coefs):
                tmp = [0] * ii + [c * elem for c in other.coefs]
                for jj in range(len(tmp)):
                    new_coefs[jj] += tmp[jj]
            return PolynomialBonus(new_coefs)
        else:
            raise TypeError()

    def __truediv__(self, other):
        if isinstance(other, MyMonomial):
            print("Not implemented yet")
        else:
            raise TypeError()

    def __rtruediv__(self, other):
        if isinstance(other, MyMonomial):
            print("Not implemented yet")
        else:
            raise TypeError()

    def __pow__(self, other):
        if isinstance(other, MyMonomial) and isinstance(other.coefficient, int) and (other.exponent == 0):
            res = PolynomialBonus(self.coefs)
            for ii in range(other.coefficient):
                res = res * self
            return res
        else:
            raise TypeError()

# =========================================================================== #
# _____________________   |Definition des fonctions |   _____________________ #
# =========================================================================== #

def binary_search_cubic_root(nb):
    """ Binary search to calcultates the cubic root of nb.
    Parameters:
    -----------
        nb [int/float]: number to dermine the cubic root.
    Return:
    -------
        cub_r : cubic root of the number nb.
    """
    if nb < 0:
        sign = -1
    else:
        sign = 1
    
    if sign * nb >= 1: 
        start = 0
        end = sign * nb
    else:
        start = sign * nb
        end = 1
    i = 0
    while True:
        cub_r = 0.5 * (start + end)
        cube = cub_r * cub_r * cub_r
        diff = sign * nb - cube
        if diff < 0:
            diff = -diff
        if diff < prec:
            return sign * cub_r
        if cube > sign * nb:
            end = cub_r
        else:
            start = cub_r
        i += 1