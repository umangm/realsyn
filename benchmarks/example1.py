#1-robot
def name():
	return '1-robot'

def problem():
	A = [[0,2],[1,0]]
	B = [[1],[1]]

	u_space = (True, [(-2, 2) for i in range(1)])

	avoid_1 = (True, [(None, -2), (None, None)] )

	avoid_2 = (True, [(10, None), (None, None)] )

	avoid_3 = (True, [(None, None), (None, -2)] )

	avoid_4 = (True, [(None, None), (10, None)] )

	avoid_5 = (True, [(4, 8), (4, 8)] )

	avoid_list = [avoid_5, avoid_1, avoid_2, avoid_3, avoid_4]

	target_mat = [[1, 0], [-1,0], [0, 1], [0, -1]]
	target_vec = [-10, 8, -10, 8]
	target_poly = (target_mat, target_vec)

	target = (True, [(8, 10), (8, 10)])

	initial_size = 0.6
	center = [1,1]
	num_steps = 10
	u_dim = 1

	avoid_dynamic = None

	Theta = (True, [(c - 0.5, c + 0.5) for c in center])

	safe_rec = None

	return initial_size, center, A, B, u_space, target, avoid_list, num_steps, u_dim, avoid_dynamic, Theta, safe_rec