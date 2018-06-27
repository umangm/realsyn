#1-robot
def name():
	return '1-robot'

def problem():
	# Discretize the navigation system at https://publish.illinois.edu/c2e2-tool/example/navigation-system/
	A = [[1,0,0,0],
	     [0,1,0,0],
	     [0,0,1,0],
	     [0,0,0,1],
	    ]

	B = [[0.1,0,0,0],
	     [0,0.1,0,0],
	     [0,0,0.1,0],
	     [0,0,0,0.1],
	     ]

	u_range = 10

	u_space = (True, [(-u_range, u_range) for i in range(4)])



	full_rank_matrix = [
					[1,0,0,0], [-1,0,0,0], 
					[0,1,0,0], [0,-1,0,0],
					[0,0,1,0], [0,0,-1,0],
					[0,0,0,1], [0,0,0,-1]
					]


	avoid_1 = (True, [(-2, 2), (-2, 2), (None, None), (None, None)] )
	avoid_2 = (True, [(None, None), (None, None), (-2, 2), (-2,2)] )


	avoid_mat_3 = [
					[1,0,-1,0],[-1,0,1,0],
					[0,1,0,-1],[0,-1,0,1]]
	avoid_vec_3 = [
					-0.5,  -0.5,
					-0.5,  -0.5
	               ]
	avoid_3 = (False, (avoid_mat_3,avoid_vec_3))
	

	avoid_list = [avoid_1, avoid_2, avoid_3]

	target = (True, [(-1,1), (4,6), (-1,1), (4,6)])


	initial_size = 1
	center = [-2,-4, 2,-4]
	num_steps = 10

	u_dim = 4

	avoid_dynamic = None

	safe_rec = None

	Theta = (True, [(-2.5, -1.5), (-4.5, -3.5), (1.5, 2.5), (-4.5, -3.5)])

	return initial_size, center, A, B, u_space, target, avoid_list, num_steps,u_dim, avoid_dynamic, Theta, safe_rec