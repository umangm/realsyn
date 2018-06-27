from util_constraints import *

z3_precision = 20
option_initial = True
option_center = True

def get_avoid_constraint_rect(em, interval_list, avoid_list):
	#interval_list = [(lo_1, hi_1), (lo_2, hi_2), ..., (lo_k, hi_k)] represents a polytope, with k = dimension of the state space.
	dim = len(interval_list)
	corner_list = set(list(itertools.product(*interval_list)))

	list_of_constraints = []
	for avoid in avoid_list:
		(avoid_flag, avoid_desc) = avoid
		if avoid_flag:
			list_of_constraints.append(get_disjointness_constraint_rect(em, dim, interval_list, avoid_desc))
		else:
			list_of_constraints.append(get_disjointness_constraint_poly_incomplete(em, dim, corner_list, avoid_desc))
	return get_cvc4_and(em, list_of_constraints)

def add_constraints(s, em, x, u, r, Theta, radius_list, x_dim, A, u_dim, B, u_space, target, avoid_list, avoid_list_dynamic, initial_rectangle, num_steps):
	#s is a cvc4 Solver
	#x, u and r are z3 variables
	#Theta, is the inital set
	#radius_list = [lst_1, lst_2, ..., lst_m], where m= num_steps, and each lst_i = [r1, ..., r_k], k = x_dim is the per-dimension constant factor to be multiplied at the i'th step
	#A is a constant square matrix of dimension x_dim \times x_dim
	#u_dim is the dimension of the input space
	#B is the feedback matrix of dimension x_dim\times u_dim
	#u_poly = (u_mat, u_vec) represents the space of inputs. That is, we allow any u that satisfies u_mat\times u + u_vec <= 0
	#target_poly = (target_mat, target_vec) is the target polytope
	#avoid_list is a list [(flag1, poly1), (flag2, poly2) ...  (flagk, polyk)], where flagi = True means rectangle, o/w general polytope. if flagi = True, thn polyi = list of x_dim pairs (hi, low). O/w it is (Ai, bi).

	is_dynamic_list_None = (avoid_list_dynamic is None)

	formula = em.mkBoolConst(True)

	formula = em.mkExpr(CVC4.AND, formula, get_avoid_constraint_rect(em, initial_rectangle, avoid_list if is_dynamic_list_None else avoid_list + avoid_list_dynamic[0]))

	(u_space_flag, u_space_desc) = u_space

	for i in range(num_steps):
		u_i_constraint = get_point_membership_constraint(em, u[i], u_space)
		next_x_constraint = get_next_constraint_point(em, x[i], u[i], A, B, x_dim, u_dim, x[i+1])
		r_lst = [em.mkExpr(CVC4.MULT, get_cvc4_const(em, radius_list[i+1][j]), r) for j in range(x_dim)]
		reach_interval_list = [(em.mkExpr(CVC4.MINUS, x[i+1][j], r_lst[j]), em.mkExpr(CVC4.PLUS, x[i+1][j], r_lst[j])) for j in range(x_dim)]
		safety_constraint = get_avoid_constraint_rect(em, reach_interval_list, avoid_list if is_dynamic_list_None else avoid_list + avoid_list_dynamic[i+1])

		formula = em.mkExpr(CVC4.AND, formula, u_i_constraint)
		formula = em.mkExpr(CVC4.AND, formula, next_x_constraint)
		formula = em.mkExpr(CVC4.AND, formula, safety_constraint)

	r_numsteps = [em.mkExpr(CVC4.MULT, get_cvc4_const(em, r_i), r) for r_i in radius_list[num_steps]]
	reach_rect = [(em.mkExpr(CVC4.MINUS, c_i, r_i_mult_r), em.mkExpr(CVC4.PLUS, c_i, r_i_mult_r)) for (c_i, r_i_mult_r) in zip(x[num_steps],r_numsteps)]
	reach_constraint = get_rect_containment_constraint(em, reach_rect, target)
	formula = em.mkExpr(CVC4.AND, formula, reach_constraint)
	s.assertFormula(formula)

def add_constraints_safety(s, em, x, u, r, Theta, radius_list, x_dim, A, u_dim, B, u_space, target, safe, initial_rectangle, num_steps):
	#s is a z3 Solver
	#x, u and r are z3 variables
	#Theta, is the inital set
	#radius_list = [lst_1, lst_2, ..., lst_m], where m= num_steps, and each lst_i = [r1, ..., r_k], k = x_dim is the per-dimension constant factor to be multiplied at the i'th step
	#A is a constant square matrix of dimension x_dim \times x_dim
	#u_dim is the dimension of the input space
	#B is the feedback matrix of dimension x_dim\times u_dim
	#u_poly = (u_mat, u_vec) represents the space of inputs. That is, we allow any u that satisfies u_mat\times u + u_vec <= 0
	#target_poly = (target_mat, target_vec) is the target polytope
	#safe is the safety set (invariant for the system)

	s.assertFormula(get_rect_containment_constraint(em, initial_rectangle, safe))

	(u_space_flag, u_space_desc) = u_space
	(safe_flag, safe_desc) = safe

	for i in range(num_steps):
		u_i_constraint = get_point_membership_constraint(em, u[i], u_space)
		next_x_constraint = get_next_constraint_point(em, x[i], u[i], A, B, x_dim, u_dim, x[i+1])
		r_lst = [em.mkExpr(CVC4.MULT, get_cvc4_const(em, radius_list[i+1][j]), r) for j in range(x_dim)]
		reach_interval_list = [(em.mkExpr(CVC4.MINUS, x[i+1][j], r_lst[j]), em.mkExpr(CVC4.PLUS, x[i+1][j], r_lst[j])) for j in range(x_dim)]
		safety_constraint = get_rect_containment_constraint(em, reach_interval_list, safe)

		s.assertFormula(u_i_constraint)
		s.assertFormula(next_x_constraint)
		s.assertFormula(safety_constraint)

	r_numsteps = [em.mkExpr(CVC4.MULT, get_cvc4_const(em, r_i), r) for r_i in radius_list[num_steps]]
	reach_rect = [(em.mkExpr(CVC4.MINUS, c_i, r_i_mult_r), em.mkExpr(CVC4.PLUS, c_i, r_i_mult_r)) for (c_i, r_i_mult_r) in zip(x[num_steps],r_numsteps)]
	reach_constraint = get_rect_containment_constraint(em, reach_rect, target)
	s.assertFormula(reach_constraint) 

def add_radius_constraint(s, em, r, r_star):
	s.assertFormula(em.mkExpr(CVC4.GEQ, r,r_star))

def add_cover_constraint(s, em, c, x0, initial_rectangle):
	if option_initial:
		s.assertFormula(em.mkExpr(CVC4.NOT, get_point_membership_constraint(em, x0, c)))
		(c_flag, c_desc) = c
		if not c_flag:
			print("How come cover is not a rectangle???")
	else:
		s.assertFormula(get_avoid_constraint_rect(em, initial_rectangle, [c]))

def add_Theta_constraint(s, em, Theta, x0, firstTime):
	(Theta_flag, Theta_description) = Theta
	x_dim = len(x0)
	if option_center and Theta_flag and firstTime:
		center = [get_cvc4_const(em, (lo+hi)/2) for (lo, hi) in Theta_description]
		for i in range(x_dim):
			s.assertFormula(em.mkExpr(CVC4.EQUAL, x0[i], center[i]))
	else:
		s.assertFormula(get_point_membership_constraint(em, x0, Theta))