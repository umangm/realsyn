from yices import *
import itertools
from fractions import Fraction

def get_yices_const(float_val):
	if float_val is None:
		return None
	f = Fraction(float_val).limit_denominator(100000000)
	return yices_rational64(f.numerator, f.denominator)

def get_yices_sum(lst_expr):
	s = yices_zero()
	for l in lst_expr:
		s = yices_add(s, l)
	return s

def get_yices_and(lst_expr):
	f = yices_true()
	for l in lst_expr:
		f = yices_and2(f, l)
	return f

def get_yices_or(lst_expr):
	f = yices_false()
	for l in lst_expr:
		f = yices_or2(f, l)
	return f

def get_matrix_multiplication_constraint(A, x, y, m, n):
	# A is a m\times n constant matrix
	# x is n\times 1 a vector
	# y is a m\times 1 vector, so that Ax = y
	list_of_constraints = []
	for i in range(m):
		lst_expr = [yices_mul(get_yices_const(A[i][j]), x[j]) for j in range(n)]
		sum_constr = get_yices_sum(em, lst_expr)
		constraint = yices_arith_eq_atom(sum_constr, y[i])
		# constraint = Sum([A[i][j]*x[j] for j in range(n)]) == y[i]
		list_of_constraints.append(constraint)
	# print(list_of_constraints)
	return list_of_constraints

def get_point_polytope_membership_constraint(x, poly):
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
		lst_expr = [yices_mul(get_yices_const(A[i][j]), x[j]) for j in range(n)] + [get_yices_const(b[i])]
		sum_constr = get_yices_sum(lst_expr)
		constraint = yices_arith_leq_atom(sum_constr, yices_zero())
		list_of_constraints.append(constraint)
	return get_yices_and(list_of_constraints)

def get_point_rectangle_membership_constraint(x, rect):
	#Dimension of x is n\times 1
	#Dimension of A is m\times n
	#Dimension of b is m\times 1
	#Returns constraints representing A\times x + b <= 0
	list_of_constraints = []
	i = 0
	for (lo, hi) in rect:
		if not (hi is None):
			list_of_constraints.append(yices_arith_leq_atom(x[i], get_yices_const(hi)))
		if not (lo is None):
			list_of_constraints.append(yices_arith_geq_atom(x[i], get_yices_const(lo)))
		i = i+1
	return get_yices_and(list_of_constraints)

def get_point_membership_constraint(x, rect_or_poly):
	#asserts that x is inside rect_or_poly
	(flag, desc) = rect_or_poly
	if flag:
		return get_point_rectangle_membership_constraint(x, desc)
	else:
		return get_point_polytope_membership_constraint(x, desc)

def get_disjointness_constraint_poly_incomplete(x_dim, cornerList_P1, P2):
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
			lst_expr = [yices_mul(get_yices_const(A[i][j]), v[j]) for j in range(x_dim)] + [get_yices_const(b[i])]
			sum_constr = get_yices_sum(lst_expr)
			l.append(yices_arith_gt_atom(sum_constr, yices_zero()))
		list_of_constraints.append(get_yices_and(l))

	return get_yices_or(list_of_constraints)

def get_disjointness_constraint_rect(x_dim, rect_1, rect_2):
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
		lo_i_2 = get_yices_const(rect_2[i][0])
		hi_i_2 = get_yices_const(rect_2[i][1])
		if(not(lo_i_2 is None)):
			list_of_constraints.append(yices_arith_lt_atom(hi_i_1,lo_i_2))
		if(not(hi_i_2 is None)):
			list_of_constraints.append(yices_arith_gt_atom(lo_i_1, hi_i_2))

	return get_yices_or(list_of_constraints)

def get_rect_poly_containment_constraint(rect, poly):
	#rect = [(lo_1, hi_1), (lo_2, hi_2), ..., (lo_k, hi_k)] represents a polytope, with k = dimension of the state space.
	#target_poly = (target_mat, target_vec) is the target polyhedron
	#We will check if each of the vertices of the reach set is inside the target polyhedron
	#poly is assumed to be consts
	corner_list = set(list(itertools.product(*rect)))

	list_of_constraints = [get_point_polytope_membership_constraint(corner, poly) for corner in corner_list]
	return get_yices_and(list_of_constraints)

def get_rect_rect_containment_constraint(rect1, rect2):
	#rect1 and rect2 = [(lo_1, hi_1), (lo_2, hi_2), ..., (lo_k, hi_k)] represents a polytope, with k = dimension of the state space.
	#We will check if in each of the dimensions, rect1 \subseteq rect2
	#rect1 is assumed to be bounded

	dim = len(rect1)

	list_of_constraints = []
	for i in range(dim):
		(lo1, hi1) = rect1[i]
		(lo2, hi2) = (get_yices_const(rect2[i][0]), get_yices_const(rect2[i][1]))
		if not(lo2 is None):
			list_of_constraints.append(yices_arith_leq_atom(lo2, lo1))
		if not(hi2 is None):
			list_of_constraints.append(yices_arith_leq_atom(hi1, hi2))
	return get_yices_and(list_of_constraints)

def get_rect_containment_constraint(rect, rect_or_poly):
	#asserts that rect is contained inside rect_or_poly
	(flag, desc) = rect_or_poly
	if flag:
		return get_rect_rect_containment_constraint(rect, desc)
	else:
		return get_rect_poly_containment_constraint(rect, desc)

def get_next_constraint_point(x, u, A, B, x_dim, u_dim, next_x):
	list_of_constraints = []
	for i in range(x_dim):
		lst_expr = [yices_mul(get_yices_const(A[i][j]), x[j]) for j in range(x_dim)] + [yices_mul(get_yices_const(B[i][j]), u[j]) for j in range(u_dim)]
		constraint = yices_arith_eq_atom(get_yices_sum(lst_expr), next_x[i])
		list_of_constraints.append(constraint)
	return get_yices_and(list_of_constraints)

def check_covered(dim, set1, list_of_covers):
	real_t = yices_real_type()
	config = yices_new_config()
	yices_default_config_for_logic(config, "QF_LRA")
	yices_set_config(config, "mode", "push-pop")
	context = yices_new_context(config)

	x = [yices_new_uninterpreted_term(real_t) for j in range(dim)]
	list_of_constraints = []

	#x \in set1
	list_of_constraints.append(get_point_membership_constraint(x, set1))

	#x is not in any of the covers
	for cover in list_of_covers:
		list_of_constraints.append(yices_not(get_point_membership_constraint(x, cover)))

	yices_assert_formula(context, get_yices_and(list_of_constraints))
	chk = yices_check_context(context, None)

	ret = False
	if(chk == STATUS_SAT):
		ret = False
	else:
		ret = True

	yices_free_context(context)	
	yices_free_config(config)

	return ret


def get_point_polytope_membership_constraint_z3(x, poly):
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
		constraint = Sum([A[i][j]*x[j] for j in range(n)]) + b[i] <= 0
		list_of_constraints.append(constraint)
	return And(list_of_constraints)

def get_point_rectangle_membership_constraint_z3(x, rect):
	#Dimension of x is n\times 1
	#Dimension of A is m\times n
	#Dimension of b is m\times 1
	#Returns constraints representing A\times x + b <= 0
	list_of_constraints = []
	i = 0
	for (lo, hi) in rect:
		if not (hi is None):
			list_of_constraints.append(x[i] <= hi)
		if not (lo is None):
			list_of_constraints.append(x[i] >= lo)
		i = i+1
	return And(list_of_constraints)

def get_point_membership_constraint_z3(x, rect_or_poly):
	#asserts that x is inside rect_or_poly
	(flag, desc) = rect_or_poly
	if flag:
		return get_point_rectangle_membership_constraint_z3(x, desc)
	else:
		return get_point_polytope_membership_constraint_z3(x, desc)

def check_covered_z3(dim, set1, list_of_covers):
	x = [Real("x_[%s]" %(j+1)) for j in range(dim)]
	list_of_constraints = []

	#x \in set1
	list_of_constraints.append(get_point_membership_constraint_z3(x, set1))

	#x is not in any of the covers
	for cover in list_of_covers:
		list_of_constraints.append(Not(get_point_membership_constraint_z3(x, cover)))

	s_cover = Solver()
	s_cover.add(And(list_of_constraints))
	chk = s_cover.check()
	if(chk == sat):
		return False
	elif(chk == unsat):
		return True
	else:
		#Some problem
		print("There has been some problem in checking if the initial set has been covered")
		return None