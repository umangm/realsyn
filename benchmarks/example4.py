#1-car-dynamic-avoid
def name():
	return '1-car dynamic avoid'

def problem():
	# Discretize the navigation system at https://publish.illinois.edu/c2e2-tool/example/navigation-system/
	A = [[1,0,0.1,0],
	     [0,1,0,0.1],
	     [0,0,0.8870, 0.0089],
	     [0,0, 0.0089, 0.8870]
	    ]

	B = [[0,0],[0,0],[1,0],[0,1]]

	u_range = 8


	u_space = (True, [(-u_range, u_range) for i in range(2)])

	avoid_1 = (True, [(None, -3.5), (None, None), (None, None), (None, None)])
	avoid_2 = (True, [(3.5, None), (None, None), (None, None), (None, None)])

	avoid_list = [avoid_1, avoid_2]

	num_steps = 15

	dynamic_list = []
	s_x = 2.5
	s_y = 0
	delta_y = 1
	r_x = 0.8
	r_y = 0.5
	for i in range(num_steps+1):
		avoid_i = (True, [(s_x-r_x, s_x+r_x), (s_y-r_y, s_y+r_y), (None, None), (None, None)])
		dynamic_list.append([avoid_i])
		s_y = s_y + delta_y



	target = (True, [(1.5, 3.5), (17, 25), (None, None), (None, None)])

	initial_size = 0.5
	center = [2.5,-3,0,0]
	

	u_dim = 2

	Theta = (True, [(2.0, 3.0), (-3.5, -2.5), (0, 0), (0, 0)])

	safe_rec = None

	return initial_size, center, A, B, u_space, target, avoid_list, num_steps,u_dim, dynamic_list, Theta, safe_rec