from CVC4 import ExprManager, SmtEngine, SExpr, Rational
import CVC4
import itertools
from fractions import Fraction

def get_cvc4_const(em, float_val):
	if float_val is None:
		return None
	f = Fraction(float_val).limit_denominator(100000000)
	return em.mkConst(Rational(f.numerator, f.denominator))

def get_cvc4_sum(em, lst_expr):
	assert not(lst_expr == []), "list is empty"
	if len(lst_expr) == 1:
		return lst_expr[0]
	else:
		return em.mkExpr(CVC4.PLUS, lst_expr)

def get_cvc4_and(em, lst_expr):
	assert not(lst_expr == []), "list is empty"
	if len(lst_expr) == 1:
		return lst_expr[0]
	else:
		return em.mkExpr(CVC4.AND, lst_expr)

def get_cvc4_or(em, lst_expr):
	assert not(lst_expr == []), "list is empty"
	if len(lst_expr) == 1:
		return lst_expr[0]
	else:
		return em.mkExpr(CVC4.OR, lst_expr)

def get_matrix_multiplication_constraint(em, A, x, y, m, n):
	# A is a m\times n constant matrix
	# x is n\times 1 a vector
	# y is a m\times 1 vector, so that Ax = y
	list_of_constraints = []
	for i in range(m):
		lst_expr = [em.mkExpr(CVC4.MULT, get_cvc4_const(em, A[i][j]), x[j]) for j in range(n)]
		sum_constr = get_cvc4_sum(em, lst_expr)
		constraint = em.mkExpr(CVC4.EQUAL, sum_constr, y[i])
		list_of_constraints.append(constraint)
	return list_of_constraints

def get_point_polytope_membership_constraint(em, x, poly):
	#Dimension of x is n\times 1
	#Dimension of A is m\times n
	#Dimension of b is m\times 1
	#Returns constraints representing A\times x + b <= 0

	A = poly[0]
	b = poly[1]
	m = len(A)
	n = len(x)

	list_of_constraints = []
	for i in range(m):
		lst_expr = [em.mkExpr(CVC4.MULT, get_cvc4_const(em, A[i][j]), x[j]) for j in range(n)] + [get_cvc4_const(b[i])]
		sum_constr = get_cvc4_sum(em, lst_expr)
		constraint = em.mkExpr(CVC4.LEQ, sum_constr, get_cvc4_const(em, 0))
		list_of_constraints.append(constraint)
	return get_cvc4_and(em, list_of_constraints)

def get_point_rectangle_membership_constraint(em, x, rect):
	#Dimension of x is n\times 1
	#Dimension of A is m\times n
	#Dimension of b is m\times 1
	#Returns constraints representing A\times x + b <= 0
	list_of_constraints = []
	i = 0
	for (lo, hi) in rect:
		if not (hi is None):
			list_of_constraints.append(em.mkExpr(CVC4.LEQ, x[i], get_cvc4_const(em, hi)))
		if not (lo is None):
			list_of_constraints.append(em.mkExpr(CVC4.GEQ, x[i], get_cvc4_const(em, lo)))
		i = i+1
	return get_cvc4_and(em, list_of_constraints)

def get_point_membership_constraint(em, x, rect_or_poly):
	(flag, desc) = rect_or_poly
	if flag:
		return get_point_rectangle_membership_constraint(em, x, desc)
	else:
		return get_point_polytope_membership_constraint(em, x, desc)

def get_disjointness_constraint_poly_incomplete(em, x_dim, cornerList_P1, P2):
	#cornerList_P1 is the list of corners of the 1st polytope. 
	#P2 = (A, b) is a polytope 
	#x_dim is the number entries in rect_1 and in rect_2
	#We have to assert that rect1 \cap P2 is empty

	A = P2[0]
	b = P2[1]
	m = len(b)

	list_of_constraints = []
	for i in range(m):
		l = []
		for v in cornerList_P1:
			lst_expr = [em.mkExpr(CVC4.MULT, get_cvc4_const(em, A[i][j]), v[j]) for j in range(x_dim)] + [get_cvc4_const(em, b[i])]
			sum_constr = get_cvc4_sum(em, lst_expr)
			l.append(em.mkExpr(CVC4.GT, sum_constr, get_cvc4_const(em, 0)))
		list_of_constraints.append(get_cvc4_and(em, l))

	return get_cvc4_or(em, list_of_constraints)

def get_disjointness_constraint_rect(em, x_dim, rect_1, rect_2):
	#rect_1 = [(lo1, hi1), ...., (lok, hik)] is a rectangle 
	#rect_2 = [(lo1, hi1), ...., (lok, hik)] is a rectangle 
	#None stands for + or - infty as appropriate
	#x_dim is the number entries in rect_1 and in rect_2
	#We have to assert that rect1 \cap rect2 is empty
	#rect_2 is all consts

	list_of_constraints = []
	for i in range(x_dim):
		lo_i_1 = rect_1[i][0]
		hi_i_1 = rect_1[i][1]
		lo_i_2 = get_cvc4_const(em,rect_2[i][0])
		hi_i_2 = get_cvc4_const(em,rect_2[i][1])
		if(not(lo_i_2 is None)):
			list_of_constraints.append(em.mkExpr(CVC4.LT, hi_i_1,lo_i_2))
		if(not(hi_i_2 is None)):
			list_of_constraints.append(em.mkExpr(CVC4.GT, lo_i_1, hi_i_2))

	return get_cvc4_or(em, list_of_constraints)

def get_rect_poly_containment_constraint(em, rect, poly):
	#rect = [(lo_1, hi_1), (lo_2, hi_2), ..., (lo_k, hi_k)] represents a polytope, with k = dimension of the state space.
	#target_poly = (target_mat, target_vec) is the target polyhedron
	#We will check if each of the vertices of the reach set is inside the target polyhedron
	#poly is assumed to be consts
	corner_list = set(list(itertools.product(*rect)))

	list_of_constraints = [get_point_polytope_membership_constraint(em, corner, poly) for corner in corner_list]
	return get_cvc4_and(em, list_of_constraints)

def get_rect_rect_containment_constraint(em, rect1, rect2):
	#rect1 and rect2 = [(lo_1, hi_1), (lo_2, hi_2), ..., (lo_k, hi_k)] represents a polytope, with k = dimension of the state space.
	#We will check if in each of the dimensions, rect1 \subseteq rect2
	#rect1 is assumed to be bounded

	dim = len(rect1)

	list_of_constraints = []
	for i in range(dim):
		(lo1, hi1) = rect1[i]
		(lo2, hi2) = (get_cvc4_const(em, rect2[i][0]), get_cvc4_const(em, rect2[i][1]))
		if not(lo2 is None):
			list_of_constraints.append(em.mkExpr(CVC4.LEQ, lo2, lo1))
		if not(hi2 is None):
			list_of_constraints.append(em.mkExpr(CVC4.LEQ, hi1, hi2))
	return get_cvc4_and(em, list_of_constraints)

def get_rect_containment_constraint(em, rect, rect_or_poly):
	(flag, desc) = rect_or_poly
	if flag:
		return get_rect_rect_containment_constraint(em, rect, desc)
	else:
		return get_rect_poly_containment_constraint(em, rect, desc)

def get_next_constraint_point(em, x, u, A, B, x_dim, u_dim, next_x):
	list_of_constraints = []
	for i in range(x_dim):
		lst_expr = [em.mkExpr(CVC4.MULT, get_cvc4_const(em, A[i][j]), x[j]) for j in range(x_dim)] + [em.mkExpr(CVC4.MULT, get_cvc4_const(em, B[i][j]), u[j]) for j in range(u_dim)]
		constraint = em.mkExpr(CVC4.EQUAL, get_cvc4_sum(em, lst_expr), next_x[i])
		list_of_constraints.append(constraint)
	return get_cvc4_and(em, list_of_constraints)


def check_covered(dim, set1, list_of_covers):
	em = ExprManager()
	s_cover = SmtEngine(em)
	real_type = em.realType()

	x = [em.mkVar("x_[%s]" %(j+1), real_type) for j in range(dim)]
	list_of_constraints = []

	#x \in set1
	list_of_constraints.append(get_point_membership_constraint(em, x, set1))

	#x is not in any of the covers
	for cover in list_of_covers:
		list_of_constraints.append(em.mkExpr(CVC4.NOT, get_point_membership_constraint(em, x, cover)))

	s_cover.assertFormula(get_cvc4_and(em, list_of_constraints))
	chk = s_cover.checkSat()
	if(chk == 1):
		return False
	else:
		return True
