#1-car-navigation
def name():
	return '1-car navigation'

def problem():
	# Discretize the navigation system at https://publish.illinois.edu/c2e2-tool/example/navigation-system/
	A = [[1,0,0.1,0],
	     [0,1,0,0.1],
	     [0,0,0.8870, 0.0089],
	     [0,0, 0.0089, 0.8870]
	    ]

	B = [[0,0],[0,0],[1,0],[0,1]]

	u_range = 5

	u_space = (True, [(-u_range, u_range) for i in range(2)])

	avoid_5 = (True, [(-2, 5), (-5, 3), (None, None), (None, None)])

	avoid_list = [avoid_5]


	target = (True, [(1,4), (3,6), (None, None), (None, None)])



	initial_size = 0.8
	center = [-3,-3,0,0]
	num_steps = 10

	u_dim = 2

	avoid_dynamic = None

	Theta = (True, [(c - 0.5, c + 0.5) for c in [-3,-3]] + [(0, 0), (0, 0)])

	safe_rec = (True, [(-5, 5), (-5, 5), (None, None), (None, None)])

	return initial_size, center, A, B, u_space, target, avoid_list, num_steps,u_dim, avoid_dynamic, Theta, safe_rec