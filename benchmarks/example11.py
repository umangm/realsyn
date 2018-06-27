#Example
def name():
	return 'example'

def problem():
	A = [[2.6207, -1.1793, 0.65705],[2,0,0],[0, 0.5, 0]]
	B = [[8],[0],[0]]

	# u_mat = [[1], [-1]]
	# u_vec = [-10, -10]
	# u_space = (False, (u_mat, u_vec))
	u_space = (True, [(-10, 10)])

	reach_bound = 4.0

	safe = (True,[(-1*reach_bound, reach_bound) for i in range(3)])


	# avoid_list = Rectangle_Safe_to_Unsafe(safe)
	avoid_list = None


	target_poly = safe

	initial_size = 1.0
	center = [0,0,0]
	num_steps = 10
	u_dim = 1

	avoid_dynamic = None

	Theta = (True, [(-0.9, 0.9), (-0.9, 0.9), (-0.9, 0.9)] )

	# P, radius_dim, num_steps, lam = get_overapproximate_rectangles(A, B, 10, num_steps)
	# print radius_dim

	return initial_size, center, A, B, u_space, target_poly, avoid_list, num_steps, u_dim, avoid_dynamic, Theta, safe
