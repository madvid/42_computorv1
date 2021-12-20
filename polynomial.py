# =========================================================================== #
# ____________________  |Importation des lib/packages|   ____________________ #
# =========================================================================== #
from tokens import Token

# =========================================================================== #
# _____________________   |Definition des constantes|   _____________________ #
# =========================================================================== #
from constants import YELLOW, END
prec = 1e-7

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
                res = Polynomial(_conv_tokens_2_lst_(self, other))
                return res
        elif isinstance(other, Polynomial):
            return other + self
        else:
            raise TypeError()

    def __radd__(self, other):
        if isinstance(other, MyMonomial):
            if  self.exponent == other.exponent:
                res = MyMonomial(other.coefficient + self.coefficient, self.exponent)
            else:
                res = Polynomial(_conv_tokens_2_lst_(other, self))
            return res
        else:
            raise TypeError()

    def __sub__(self, other):
        if isinstance(other, MyMonomial):
            if self.exponent == other.exponent:
                res = MyMonomial(self.coefficient - other.coefficient, self.exponent)
            else:
                other.coefficient = - other.coefficient
                res = Polynomial(_conv_tokens_2_lst_(self, other))
            return res
        elif isinstance(other, Polynomial):
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
                res = Polynomial(_conv_tokens_2_lst_(other, self))
            return res
        else:
            raise TypeError()

    def __mul__(self, other):
        if isinstance(other, MyMonomial):
            res = MyMonomial(other.coefficient * self.coefficient, self.exponent + other.exponent)
            return res
        elif isinstance(other, Polynomial):
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


class Polynomial():

    def __init__(self, lst_coefs):
        """Creates the polynomial instance based on the list of coefficients.
        Remark:
        -------
            Coefficients in the list are ordered from the coef of the highest
            MyMonomial degree to the MyMonomial of degree 0 (i.e. scalar constant)
        Example:
        --------
            polynomial expr: a.Xˆ3 + b.X ˆ2 + c.X + d => [a, b, c, d]
        Note:
        -----
            There is no gap in coefficient, meaning that a polynomial expr
            without a specific MyMonomial of degree i has still its coefficient
            in list_coeff but it is set to zero.
            a.X^3 + b => [b, 0, 0, a]
        """
        self.coefs = lst_coefs
        while len(self.coefs) > 1 and self.coefs[-1] == 0:
            self.coefs = self.coefs[:-1]
        self.degree = len(self.coefs) - 1

    def _zero_degree_resolution_(self):
        """Calculates the roots of polynomial of degree 0.
        Return:
        -------
            * r [floats]: roots of the polynomial.
        """
        if self.degree == 0:
            a = self.coefs[0]
            if a == 0:
                r = 0
            if a != 0:
                r = None
            return [r]
        else:
            s_raise = "Polynomial is not of 0th degree."

    
    def _first_degree_resolution_(self):
        """Calculates the roots of polynomial of degree 1.
        Return:
        -------
            * r [floats]: roots of the polynomial.
        """
        if self.degree == 1:
            a = self.coefs[1]
            b = self.coefs[0]
            r = -b / a
            return [r]
        else:
            s_raise = "Polynomial is not of 1st degree."
            raise Exception(s_raise)

    def discriminant(self) -> float:
        """ Calculates the discriminant of the polynomial.
        Parameters:
        -----------
            * self [SecondOrderPolynomial class object]: ...

        Return:
        -------
            delta [float]: value of the discriminant constituted of tkn_m1/2/3.
        """
        if self.degree == 2:
            a = self.coefs[2]
            b = self.coefs[1]
            c = self.coefs[0]
            delta = b * b - 4 * a * c
            return delta
        elif self.degree == 3:
            a = self.coefs[3]
            b = self.coefs[2]
            c = self.coefs[1]
            d = self.coefs[0]
            delta = 18 * a * b * c * d - 4 * power(b, 3) * d + power(b * c, 2) \
                - 4 * a * power(c, 3) - 27 * power(a * d, 2)
            return delta
        else:
            s_raise = "discriminant implementation for 2nd degree polynomial."
            raise Exception(s_raise)


    def _second_degree_resolution_(self):
        """Calculates the roots of polynomial of degree 2.
        Return:
        -------
            * r1, r2 / r [floats/complexes]: roots of the polynomial.
        """
        if self.degree == 2:
            delta = self.discriminant()
            a = self.coefs[2]
            b = self.coefs[1]
            if delta > 0:
                r1 = 0.5 * (-b - babylonian_sqrt(delta)) / a
                r2 = 0.5 * (-b + babylonian_sqrt(delta)) / a
                return [r1, r2]
            elif delta == 0:
                return [(- 0.5 * b / a)]
            else:
                real = - 0.5 * b / a
                imaginary = 0.5 * babylonian_sqrt(-delta) / a
                r1 = complex(real, -imaginary)
                r2 = complex(real, imaginary)
                return [r1, r2]
        else:
            s_raise = "Polynomial is not of 2nd degree."
            raise Exception(s_raise)


    def _third_degree_resolution_(self):
        """ Calculates the roots of polynomial of degree 3.
        The function is here for the completeness of the class and avoid
        the redefinition of the some methods in the class PolynomialBonus.
        """
        # reference: https://fr.wikiversity.org/wiki/Équation_du_troisième_degré/Méthode_de_Cardan
        if self.degree == 3:
            msg = "3rd degree resolution is a project's bonus. " \
                + "Use instance of class PolynomialBonus to have access to " \
                + "to the resolution of 3rd degree polynomial."
            print(YELLOW + msg + END)
            return []
        else:
            print("Polynomial is not of 3rd degree.")


    def polynomial_roots(self):
        """Calculates the roots of the polynomial.
        Return:
        -------
            delta [float]: value of the discriminant constituted of tkn_m1/2/3.
        """
        roots = None
        if self.degree == 0:
            roots = self._zero_degree_resolution_()
        if self.degree == 1:
            roots = self._first_degree_resolution_()
        if self.degree == 2:
            roots = self._second_degree_resolution_()
        if self.degree == 3:
            roots = self._third_degree_resolution_()
        self.roots = roots
        return roots


    def lambda_polynom(self):
        """ Constructs the lambda function f corresponding to the polynomial.
        Return:
        -------
            f [lambda function]: polynomial function.
        """
        lst_p = list(range(len(self.coefs)))
        f = lambda x: sum([a * power(x, p) for a, p in zip(self.coefs, lst_p)])
        self.lambda_p = f
        return f


    def lambda_first_derivative(self):
        """ Constructs the lambda function df corresponding to the polynomial
        first derivative.
        Return:
        -------
            df [lambda function]: polynomial derivative function.
        """
        lst_p = list(range(len(self.coefs)))
        lst_p = lst_p[1:]
        d_coefs = self.coefs[1:]
        print(f"valeurs de coeffs: {self.coeffs} --- valeurs de d_coeffs = {d_coefs}")
        print(f"valeurs de lst_p = {lst_p}")
        df = lambda x: sum([a * p * power(x, p - 1) for a, p in zip(d_coefs, lst_p)])
        self.lambda_dp = df
        return df


    def lambda_second_derivative(self):
        """ Constructs the lambda function d2f corresponding to the polynomial
        second derivative.
        Return:
        -------
            d2f [lambda function : polynomial second derivative function.
        """
        lst_p = list(range(len(self.coefs)))
        lst_p = lst_p[2:]
        d2_coefs = self.coefs[2:]
        d2f = lambda x: sum([a * p * (p - 1) * power(x, p - 2) for a, p in zip(d2_coefs, lst_p)])
        self.lambda_d2p = d2f
        return d2f


    @staticmethod
    def _print_roots(roots):
        """ Displays the number in the parameter roots as string. roots
        parameter is expected to be the list of the root of a Polynomial object.
        Parameters:
        -----------
            * roots [list(float/complex)]: list of all the roots of a polynomial
                expression.
        """
        for r in roots:
            if isinstance(r, (int, float)):
                print(r)
            if isinstance(r, complex):
                if r.imag > 0:
                    print(r.real, '+', f"{r.imag}.i")
                else:
                    print(r.real, '-', f"{-r.imag}.i")


    def _summarize_degree_other(self):
        """ Displays type function.
        Function prints:
            * reduced form of the Polynomial instance.
            * natural form of the Polynomial instance.
            * degree of the Polynomial instance.
            * message that computor does not manage the roots seach for
            polynomial degree greater than 3.
        """
        print("Reduced form:".ljust(20), self.__repr__() + "= 0")
        print("Natural form:".ljust(20), self.natural_form() + "= 0")
        print("Polynomial degree:".ljust(20), self.degree)
        msg = "Resolution of polynomial equation with degree higher " \
            + "than 3 are not handle in this project."
        print(YELLOW + msg + END)
        self.roots = []


    def _summarize_degree_3(self):
        """Displays type function.
        The function is here for the completeness of the class and avoid
        the redefinition of the some methods in the class PolynomialBonus.
        """
        delta = self.discriminant()
        self.roots = []
        
        print("Reduced form:".ljust(20), self.__repr__() + "= 0")
        print("Natural form:".ljust(20), self.natural_form() + "= 0")
        print("Polynomial degree:".ljust(20), self.degree)
        print("Discriminant: ".ljust(20), delta)

        msg = "3rd degree resolution is a project's bonus. " \
                + "Use instance of class PolynomialBonus to have access to " \
                + "to the resolution of 3rd degree polynomial."
        print(YELLOW + msg + END)


    def _summarize_degree_2(self):
        """Displays type function.
        Function prints:
            * reduced form of the Polynomial instance.
            * natural form of the Polynomial.
            * degree of the Polynomial.
            * discriminant of the Polynomial.
            * roots of the Polynomial.
        """
        print("Reduced form:".ljust(20), self.__repr__() + " = 0")
        print("Natural form:".ljust(20), self.natural_form() + " = 0")
        print("Factorized form:".ljust(20), self.factorized_form() + " = 0")
        print("Canonical form:".ljust(20), self.canonical_form() + " = 0")
        print("Polynomial degree:".ljust(20), self.degree)
        delta = self.discriminant()
        print("Discriminant:".ljust(20), delta)
        roots = self.polynomial_roots()
        if delta > 0:
            print("Discriminant is positive, the two solutions are:")
        elif delta == 0:
            print("Discriminant is null, the solution is:")
        else:
            print("Discriminant is strictly negative, the two complex solutions are:")
        Polynomial._print_roots(roots)


    def _summarize_degree_1(self):
        """Displays type function.
        Function prints:
            * reduced form of the Polynomial instance.
            * natural form of the Polynomial.
            * degree of the Polynomial.
            * root of the Polynomial.
        """
        print("Reduced form:".ljust(20), self.__repr__(), "= 0")
        print("Factorized form:".ljust(20), self.factorized_form() + " = 0")
        print("Natural form:".ljust(20), self.natural_form() + " = 0")
        print("Polynomial degree:".ljust(20), self.degree)
        roots = self.polynomial_roots()
        print("The solution is:")
        Polynomial._print_roots(roots)


    def _summarize_degree_0(self):
        """Displays type function.
        Function prints:
            * reduced form of the Polynomial instance.
            * natural form of the Polynomial.
            * degree of the Polynomial.
            * root of the Polynomial when it exists.
        """
        print("Reduced form:".ljust(20), self.__repr__(), "= 0")
        print("Natural form:".ljust(20), self.natural_form() + " = 0")
        print("Polynomial degree:".ljust(20), self.degree)
        roots = self.polynomial_roots()
        if roots[0] is None:
            print("There is no solution for the zeroth order polynomial equation.")
        if roots[0] == 0:
            print("All real values of x are solution of the polynomial equation.")


    def summarize(self):
        """Displays core function.
        Calls the appropriate display function according to the polynomial degree.
        """
        if self.degree > 3:
            self._summarize_degree_other()
        elif self.degree == 3:
            self._summarize_degree_3()
        elif self.degree == 2:
            self._summarize_degree_2()
        elif self.degree == 1:
            self._summarize_degree_1()
        elif self.degree == 0:
            self._summarize_degree_0()


    def factorized_form(self):
        """ Returns the factorized expression of the polynomial expression
        in a string format.
        Return:
        -------
            s_poly [str]: factorized expression of the polynomial.
        """
        roots = self.polynomial_roots()
        signs = [c_sign_(r) for r in roots]
        
        s_poly = f"{self.coefs[-1]}"
        for sign, r in zip(signs, roots):
            if isinstance(r, (float, int)):
                if sign == '+':
                    s_poly += f" * (X - {_abs(r)})"
                else:
                    s_poly += f" * (X + {_abs(r)})"
            if isinstance(r, complex):
                if (sign[0] == '-') and (sign[1] == '-'):
                    val = [_abs(r.real), _abs(r.imag)]
                    s_poly += f" * (X + {val[0]} + {val[1]}.i)"
                elif (sign[0] == '-') and (sign[1] == '+'):
                    val = [_abs(r.real), _abs(r.imag)]
                    s_poly += f" * (X + {val[0]} - {val[1]}.i)"
                elif (sign[0] == '+') and (sign[1] == '-'):
                    val = [_abs(r.real), _abs(r.imag)]
                    s_poly += f" * (X - {val[0]} + {val[1]}.i)"
                else:
                    val = [_abs(r.real), _abs(r.imag)]
                    s_poly += f" * (X - {val[0]} - {val[1]}.i)"
        if s_poly[0:4] == "1 * ": 
            s_poly = s_poly[4:]
        return  s_poly


    def canonical_form(self):
        """ Returns the canonical expression of the polynomial expression
        in a string format.
        Return:
        -------
            s_poly [str]: canonical expression of the polynomial.
        """
        alpha = -0.5 * self.coefs[1] / self.coefs[2]
        f = self.lambda_polynom()
        beta = f(alpha)
        #beta = 0.25 * self.discriminant() / self.coefs[0]
        
        sign1 = '-'
        sign2 = '-'
        if alpha < 0:
            sign1 = '+'
        if beta < 0:
            sign2 = '+'

        alpha = _abs(alpha)
        beta = _abs(beta)
        s_poly = f"{self.coefs[-1]} * (X {sign1} {alpha})^2 {sign2} {beta}"
        if s_poly[0:5] == "1 * ":
            s_poly = s_poly[0:5]
        return s_poly


    def natural_form(self):
        """ Returns the natural expression of the polynomial expression
        in a string format.
        Return:
        -------
            s_poly [str]: natural expression of the polynomial.
        """
        s_poly = self.__repr__()
        s_poly = s_poly.replace('^1', '')
        s_poly = s_poly.replace(' * X^0', '')
        s_poly = s_poly.replace(' 1 * X', ' X')
        return s_poly

    def __add__(self, other):
        if isinstance(other, MyMonomial):
            if len(self.coefs) > other.exponent + 1:
                new_coefs = self.coefs
                new_coefs[other.exponent] += other.coefficient
            else:
                new_coefs = self.coefs + [0] * (other.exponent + 1 - self.degree)
                new_coefs[other.exponent] += other.coefficient
            return Polynomial(new_coefs)
        if isinstance(other, Polynomial):
            if self.degree >= other.degree:
                new_coefs = self.coefs
                remind = other.coefs
            else:
                new_coefs = other.coefs
                remind = self.coefs
            for ii,val in enumerate(remind):
                new_coefs[ii] += val
            return Polynomial(new_coefs)
        raise TypeError()

    def __radd__(self, other):
        if isinstance(other, MyMonomial):
            if len(self.coefs) > other.exponent + 1:
                new_coefs = self.coefs
                new_coefs[other.exponent] += other.coefficient
            else:
                new_coefs = self.coefs + [0] * (other.exponent + 1 - self.degree)
                new_coefs[other.exponent] += other.coefficient
            return Polynomial(new_coefs)
        if isinstance(other, Polynomial):
            if self.degree >= other.degree:
                new_coefs = self.coefs
                remind = other.coefs
            else:
                new_coefs = other.coefs
                remind = self.coefs
            for ii,val in enumerate(remind):
                new_coefs[ii] += val
            return Polynomial(new_coefs)
        raise TypeError()

    def __sub__(self, other):
        if isinstance(other, MyMonomial):
            if len(self.coefs) > other.exponent + 1:
                new_coefs = self.coefs
                new_coefs[other.exponent] -= other.coefficient                
            else:
                new_coefs = self.coefs + [0] * (other.exponent + 1 - self.degree)
                new_coefs[other.exponent] -= other.coefficient
            return Polynomial(new_coefs)
        if isinstance(other, Polynomial):
            if self.degree >= other.degree:
                new_coefs = self.coefs
                remind = list(map(lambda x : -x, other.coefs))
            else:
                new_coefs = list(map(lambda x : -x, other.coefs))
                remind = self.coefs
            for ii,val in enumerate(remind):
                new_coefs[ii] += val
            return Polynomial(new_coefs)
        raise TypeError()

    def __rsub__(self, other):
        if isinstance(other, MyMonomial):
            new_coefs = list(map(lambda x : -x, self.coefs))
            if len(self.coefs) > other.exponent + 1:
                new_coefs[other.exponent] += other.coefficient
            else:
                new_coefs = new_coefs + [0] * (other.exponent + 1 - self.degree)
                new_coefs[other.exponent] += other.coefficient
            return Polynomial(new_coefs)
        if isinstance(other, Polynomial):
            if self.degree >= other.degree:
                new_coefs = list(map(lambda x : -x, self.coefs))
                remind = other.coefs
            else:
                new_coefs = other.coefs
                remind = list(map(lambda x : -x, self.coefs))
            for ii,val in enumerate(remind):
                new_coefs[ii] += val
            return Polynomial(new_coefs)
        raise TypeError()

    def __mul__(self, other):
        if isinstance(other, MyMonomial):
            new_coefs = [c * other.coefficient for c in self.coefs]
            new_coefs = [0] * other.exponent + self.coefs
            return Polynomial(new_coefs)
        elif isinstance(other, Polynomial):
            new_coefs = [0] * (self.degree + other.degree + 1)
            for ii, elem in enumerate(self.coefs):
                tmp = [0] * ii + [c * elem for c in other.coefs]
                for jj in range(len(tmp)):
                    new_coefs[jj] += tmp[jj]
            return Polynomial(new_coefs)
        else:
            raise TypeError()

    def __rmul__(self, other):
        if isinstance(other, MyMonomial):
            new_coefs = [c * other.coefficient for c in self.coefs]
            new_coefs = [0] * other.exponent + self.coefs
            return Polynomial(new_coefs)
        elif isinstance(other, Polynomial):
            new_coefs = [0] * (self.degree + other.degree + 1)
            for ii, elem in enumerate(self.coefs):
                tmp = [0] * ii + [c * elem for c in other.coefs]
                for jj in range(len(tmp)):
                    new_coefs[jj] += tmp[jj]
            return Polynomial(new_coefs)
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
            res = Polynomial(self.coefs)
            for ii in range(other.coefficient):
                res = res * self
            return res
        else:
            raise TypeError()


    def __repr__(self):
        """ Returns the developped expression of the polynomial expression
        in a string format.
        Return:
        -------
            s_poly [str]: developped expression of the polynomial.
        """
        # pour afficher la forme developpée.
        lst_p = list(range(len(self.coefs)))
        sign = [sign_(c) for c in self.coefs]
        abs_val = [_abs(n) for n in self.coefs]
        if sign[0] == '+':
            sign[0] = ''
        
        if len(lst_p) == 1:
            s_poly = [f"{s} {c} * X^{p} " for s, c, p in zip(sign, abs_val, lst_p)]
        else:
            s_poly = [f"{s} {c} * X^{p} " for s, c, p in zip(sign, abs_val, lst_p) if (c != 0)]
        s_poly = ''.join(s_poly)
        if s_poly[0:5] == ' 1 * ':
            s_poly = s_poly[5:]
        if s_poly[0] == ' ':
            s_poly = s_poly[1:]
        if s_poly[-1] == ' ':
            s_poly = s_poly[:-1]
        return s_poly


# =========================================================================== #
# _____________________   |Definition des fonctions |   _____________________ #
# =========================================================================== #
def babylonian_sqrt(nb):
    """ Implementation of the Babylonian square-root algorithm.
    Parameters:
    -----------
        nb [int/float]: number to dermine the square root.
    Return:
    -------
        sqrt : square root of the number nb.
    """
    if nb < 0:
        nb *= -1
    sqrt = nb / 2
    diff = 1
    while diff > prec:
        prev_guess = sqrt
        sqrt = (sqrt + nb / sqrt) / 2
        diff = prev_guess - sqrt
        if diff < 0:
            diff = -diff
    return sqrt


def power(x,p):
    """ Elevates the number x to the power p.
    Arguments:
    ----------
        * x [int/float]: a number.
        * p [int]: the power that will elevate x.
    Return:
    -------
        * res [int/float]: result of x**p
    Why?:
    -----
        According to the project pdf, the only authhorized operations
        are '+','-','*' and '/'
    """
    i = 1
    if p == 0:
        return 1
    res = x
    while i < p:
        res *= x
        i += 1
    return res


def c_sign_(coef: int or float or complex):
    """ Returns the sign of coef.
    Parameters coef can be a int, float or complex.
    If coef is in (int, float), _sign is called, otherwise the signs
    of the real and imaginary parts are returned.
    Return:
    -------
        * '+'/'-' [str]: if coef is (int | float) and positive / negative.
        * ['+'/'-', '+'/'-'] [list]: signs of the real and imaginary part.
    """
    if isinstance(coef, (int, float)):
        return sign_(coef)
    return [sign_(coef.real), sign_(coef.imag)]


def sign_(coef:int or float) -> str:
    """ Returns the sign of coef. Parameters coef is a float or an int only.
    Return:
    -------
        * '+' [str]: if coef is positive.
        * '-' [str]: if coef is negative.
    """
    if (coef >= 0):
        return '+'
    if (coef < 0):
        return '-'


def c_abs_(nb:int or float or complex):
    """ Returns the absolute value of the coef.
    If coef is an int | float, _abs is called, otherwise absolute value
    of the real and imaginary part are returned.
    Return:
    -------
        * |nb|: if nb is an integer / float.
        * [|nb.real|, |nb.imag|]: if nb is a complex.
    """
    if isinstance(nb, (int, float)):
        return _abs(nb)
    # there is no absolue value for complex number
    return [_abs(nb.real), _abs(nb.imag)]


def _abs(nb:int or float):
    """ Returns the absolute value of the coef.
    Return:
    -------
        * |nb|.
    """
    if (nb >= 0):
        return nb
    if (nb < 0):
        return -nb


def _conv_tokens_2_lst_(monom_1:MyMonomial, monom_2:MyMonomial) -> list:
    """ Functions which converts a list of Monomial objects into the list of
    corresponding coefficients to instance Polynomial/PolynomialBonus object.
    The exponent of both of the monomials should be different.
    Parameters:
    -----------
        * args: Monomial objects.
    Return:
    -------
        * lst_coefs [list]: list of coefficients corresponding to the coefficients
          of a polynomial ordering from the lowest variable exponent to the highest.
          ([1, 0, 3] --> 1 + 0.X + 3.X^2)
    """
    if monom_1.exponent == monom_2.exponent:
        lst_coefs = [0] * (monom_1.exponent + 1)
        lst_coefs[monom_1.exponent] = monom_1.coefficient + monom_2.coefficient
    else:
        exp_max = max([monom_1.exponent, monom_2.exponent])
        lst_coefs = [0] * (exp_max + 1)
        lst_coefs[monom_1.exponent] = monom_1.coefficient
        lst_coefs[monom_2.exponent] = monom_2.coefficient
    return lst_coefs