from z3 import *
import itertools

def get_matrix_multiplication_constraint(A, x, y, m, n):
	# A is a m\times n matrix. Can be a constant or a variable matrix
	# x is n\times 1 a vector
	# y is a m\times 1 vector, so that Ax = y
	list_of_constraints = []
	for i in range(m):
		constraint = Sum([A[i][j]*x[j] for j in range(n)]) == y[i]
		list_of_constraints.append(constraint)
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
		constraint = Sum([A[i][j]*x[j] for j in range(n)]) + b[i] <= 0
		list_of_constraints.append(constraint)
	return And(list_of_constraints)

def get_point_rectangle_membership_constraint(x, rect):
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

def get_point_membership_constraint(x, rect_or_poly):
	#asserts that x is inside rect_or_poly
	(flag, desc) = rect_or_poly
	if flag:
		return get_point_rectangle_membership_constraint(x, desc)
	else:
		return get_point_polytope_membership_constraint(x, desc)

def get_disjointness_constraint(x_dim, P1, P2, str_identifier):
	#P1 is a tuple (A, b), A is m1\times x_dim representing polytope Ax + b <= 0
	#P2 is a tuple (C, d), C is m2\times x_dim representing polytope Cx + d <= 0
	#x_dim is the number of columns in A and C each
	#We have to assert (E = [A, C], f = [b, d]) is empty
	#Using Farkas Lemma, we instead have to assert that there is a y for which E^T y = 0, f^T y > 0 (and not f^T y < 0, notice how we represent polytopes) and y >= 0
	#str_identifier is just a new identifier for the new y variables introduced
	A = P1[0]
	b = P1[1]
	C = P2[0]
	d = P2[1]
	m1 = len(b) 
	m2 = len(d)
	y_dim = m1 + m2

	y = [Real(str_identifier + "_%s" %(j+1)) for j in range(y_dim)]

	list_of_constraints = []
	#First assert E^T y = 0
	for i in range(x_dim):
		lst = [A[j][i]*y[j] for j in range(m1)] + [C[j][i]*y[j+m1] for j in range(m2)]
		list_of_constraints.append(Sum(lst) == 0)

	#Next assert f^T > 0
	lst = [b[j]*y[j] for j in range(m1)] + [d[j]*y[j+m1] for j in range(m2)]
	list_of_constraints.append(Sum(lst) > 0)

	#Last, assert that y >= 0
	for j in range(y_dim):
		list_of_constraints.append(y[j] >= 0)

	return And(list_of_constraints)

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
			l.append( Sum([A[i][j]*v[j] for j in range(x_dim)]) + b[i] > 0 )
		list_of_constraints.append(And(l))

	return Or(list_of_constraints)

def get_disjointness_constraint_rect(x_dim, rect_1, rect_2):
	#rect_1 = [(lo1, hi1), ...., (lok, hik)] is a rectangle 
	#rect_2 = [(lo1, hi1), ...., (lok, hik)] is a rectangle 
	#None stands for + or - infty as appropriate
	#x_dim is the number entries in rect_1 and in rect_2
	#We have to assert that rect1 \cap rect2 is empty

	list_of_constraints = []
	for i in range(x_dim):
		lo_i_1 = rect_1[i][0]
		hi_i_1 = rect_1[i][1]
		lo_i_2 = rect_2[i][0]
		hi_i_2 = rect_2[i][1]
		if(not(lo_i_2 is None)):
			list_of_constraints.append(hi_i_1 < lo_i_2)
		if(not(hi_i_2 is None)):
			list_of_constraints.append(lo_i_1 > hi_i_2)

	return Or(list_of_constraints)

def get_rect_poly_containment_constraint(rect, poly):
	#rect = [(lo_1, hi_1), (lo_2, hi_2), ..., (lo_k, hi_k)] represents a polytope, with k = dimension of the state space.
	#target_poly = (target_mat, target_vec) is the target polyhedron
	#We will check if each of the vertices of the reach set is inside the target polyhedron
	corner_list = set(list(itertools.product(*rect)))

	list_of_constraints = []
	for corner in corner_list:
		list_of_constraints.append(get_point_polytope_membership_constraint(corner, poly))
	return And(list_of_constraints)

def get_rect_rect_containment_constraint(rect1, rect2):
	#rect1 and rect2 = [(lo_1, hi_1), (lo_2, hi_2), ..., (lo_k, hi_k)] represents a polytope, with k = dimension of the state space.
	#We will check if in each of the dimensions, rect1 \subseteq rect2
	#rect1 is assumed to be bounded

	dim = len(rect1)

	list_of_constraints = []
	for i in range(dim):
		(lo1, hi1) = rect1[i]
		(lo2, hi2) = rect2[i]
		if not(lo2 is None):
			list_of_constraints.append(lo2 <= lo1)
		if not(hi2 is None):
			list_of_constraints.append(hi1 <= hi2)
	return And(list_of_constraints)

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
		constraint = Sum([A[i][j]*x[j] for j in range(x_dim)]) + Sum([B[i][j]*u[j] for j in range(u_dim)]) == next_x[i]
		list_of_constraints.append(constraint)
	return And(list_of_constraints)

def check_covered(dim, set1, list_of_covers):
	x = [Real("x_[%s]" %(j+1)) for j in range(dim)]
	list_of_constraints = []

	#x \in set1
	list_of_constraints.append(get_point_membership_constraint(x, set1))

	#x is not in any of the covers
	for cover in list_of_covers:
		list_of_constraints.append(Not(get_point_membership_constraint(x, cover)))

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