from util_constraints import *

z3_precision = 20
option_initial = True
option_center = True

def get_avoid_constraint_rect(interval_list, avoid_list):
	#interval_list = [(lo_1, hi_1), (lo_2, hi_2), ..., (lo_k, hi_k)] represents a polytope, with k = dimension of the state space.
	dim = len(interval_list)
	corner_list = set(list(itertools.product(*interval_list)))

	list_of_constraints = []
	for avoid in avoid_list:
		(avoid_flag, avoid_desc) = avoid
		if avoid_flag:
			list_of_constraints.append(get_disjointness_constraint_rect(dim, interval_list, avoid_desc))
		else:
			list_of_constraints.append(get_disjointness_constraint_poly_incomplete(dim, corner_list, avoid_desc))
	return And(list_of_constraints)

def add_constraints(s, x, u, r, Theta, radius_list, x_dim, A, u_dim, B, u_space, target, avoid_list, avoid_list_dynamic, initial_rectangle, num_steps):
	#s is a z3 Solver
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

	s.add(get_avoid_constraint_rect(initial_rectangle, avoid_list if is_dynamic_list_None else avoid_list + avoid_list_dynamic[0]))

	(u_space_flag, u_space_desc) = u_space

	for i in range(num_steps):
		u_i_constraint = get_point_membership_constraint(u[i], u_space)
		next_x_constraint = get_next_constraint_point(x[i], u[i], A, B, x_dim, u_dim, x[i+1])
		reach_interval_list = [(x[i+1][j] - radius_list[i+1][j]*r, x[i+1][j] + radius_list[i+1][j]*r) for j in range(x_dim)]
		safety_constraint = get_avoid_constraint_rect(reach_interval_list, avoid_list if is_dynamic_list_None else avoid_list + avoid_list_dynamic[i+1])

		s.add(u_i_constraint)
		s.add(next_x_constraint)
		s.add(safety_constraint)

	reach_rect = [(c_i-r_i*r, c_i+r_i*r) for (c_i, r_i) in zip(x[num_steps],radius_list[num_steps] )]
	reach_constraint = get_rect_containment_constraint(reach_rect, target)
	s.add(reach_constraint) 

def add_constraints_safety(s, x, u, r, Theta, radius_list, x_dim, A, u_dim, B, u_space, target, safe, initial_rectangle, num_steps):
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

	s.add(get_rect_containment_constraint(initial_rectangle, safe))

	(u_space_flag, u_space_desc) = u_space
	(safe_flag, safe_desc) = safe

	for i in range(num_steps):
		u_i_constraint = get_point_membership_constraint(u[i], u_space)
		next_x_constraint = get_next_constraint_point(x[i], u[i], A, B, x_dim, u_dim, x[i+1])
		reach_interval_list = [(x[i+1][j] - radius_list[i+1][j]*r, x[i+1][j] + radius_list[i+1][j]*r) for j in range(x_dim)]
		safety_constraint = get_rect_containment_constraint(reach_interval_list, safe)

		s.add(u_i_constraint)
		s.add(next_x_constraint)
		s.add(safety_constraint)

	reach_rect = [(c_i-r_i*r, c_i+r_i*r) for (c_i, r_i) in zip(x[num_steps],radius_list[num_steps] )]
	reach_constraint = get_rect_containment_constraint(reach_rect, target)
	s.add(reach_constraint) 

def add_radius_constraint(r, s, r_star):
	s.add(r >= r_star)

def add_cover_constraint(c, x0, s, initial_rectangle):
	if option_initial:
		s.add(Not(get_point_membership_constraint(x0, c)))
		(c_flag, c_desc) = c
		if not c_flag:
			print("How come cover is not a rectangle???")
	else:
		#x_0 bloated does not intersect with any of the covering sets
		s.add(get_avoid_constraint_rect(initial_rectangle, [c]))

def add_Theta_constraint(s, Theta, x0, firstTime):
	(Theta_flag, Theta_description) = Theta
	x_dim = len(x0)
	if option_center and Theta_flag and firstTime:
		center = [(lo+hi)/2 for (lo, hi) in Theta_description]
		for i in range(x_dim):
			s.add(x0[i] == center[i])
	else:
		s.add(get_point_membership_constraint(x0, Theta))