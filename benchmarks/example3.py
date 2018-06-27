#running_example
def name():
	return 'running-example'

def problem():
	# Discretize the navigation system at https://publish.illinois.edu/c2e2-tool/example/navigation-system/
	A = [[1,0,0.1,0],
	     [0,1,0,0.1],
	     [0,0,0.8870, 0.0089],
	     [0,0, 0.0089, 0.8870]
	    ]

	B = [[0,0],[0,0],[1,0],[0,1]]

	u_range = 1.5

	u_space = (True, [(-u_range, u_range) for i in range(2)])


	avoid_1 = (True, [(None, 0), (None, None), (None, None), (None, None)])
	avoid_2 = (True, [(11, None), (None, None), (None, None), (None, None)])
	avoid_3 = (True, [(None, None), (None, 0), (None, None), (None, None)])
	avoid_4 = (True, [(None, None), (6, None), (None, None), (None, None)])
	avoid_5 = (True, [(4, 7), (3, 6), (None, None), (None, None)])
	avoid_8 = (True, [(8, 11), (3, 3.9), (None, None), (None, None)])
	avoid_9 = (True, [(4, 11), (0, 2.0), (None, None), (None, None)])

	avoid_list = [avoid_1, avoid_2, avoid_3, avoid_4, avoid_5, avoid_8, avoid_9]


	target = (True, [(9, 11), (5, 6), (None, None), (None, None)])

	initial_size = 0.4

	center = [0.5,1.5,0,0]
	num_steps = 20

	u_dim = 2

	avoid_dynamic = None

	Theta = (True, [(0.3, 0.7), (1.3, 1.7), (0, 0), (0, 0)] )

	safe_rec = None

	# plotter_room(None, None, avoid_list, target_poly)

	return initial_size, center, A, B, u_space, target, avoid_list, num_steps,u_dim, avoid_dynamic, Theta, safe_rec