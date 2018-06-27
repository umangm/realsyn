#2-car-navigation
def name():
	return '2-car navigation'

def problem():
	# Discretize the navigation system at https://publish.illinois.edu/c2e2-tool/example/navigation-system/
	A = [[1,0,0.1,0,0,0,0,0],
	     [0,1,0,0.1,0,0,0,0],
	     [0,0,0.8870, 0.0089,0,0,0,0],
	     [0,0, 0.0089, 0.8870,0,0,0,0],
	     [0,0,0,0,1,0,0.1,0],
	     [0,0,0,0,0,1,0,0.1],
	     [0,0,0,0,0,0,0.8870, 0.0089],
	     [0,0,0,0,0,0, 0.0089, 0.8870]
	    ]

	B = [[0,0,0,0],
	     [0,0,0,0],
	     [1,0,0,0],
	     [0,1,0,0],
	     [0,0,0,0],
	     [0,0,0,0],
	     [0,0,1,0],
	     [0,0,0,1],
	     ]

	u_range = 5

	u_space = (True, [(-u_range, u_range) for i in range(4)])


	avoid_1 = (True, [(-2, 2), (-2, 2), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None)] )

	avoid_2 = (True, [ (None, None), (None, None), (None, None), (None, None), (-2, 2), (-2, 2), (None, None), (None, None)] )


	avoid_mat_3 = [[1,0,0,0,-1,0,0,0],[-1,0,0,0,1,0,0,0],[0,1,0,0,0,-1,0,0],[0,-1,0,0,0,1,0,0]]
	avoid_vec_3 = [
					-0.5,  -0.5,
					-0.5,  -0.5
	               ]

	avoid_3 = (False, (avoid_mat_3,avoid_vec_3))
	avoid_list = [avoid_1, avoid_2, avoid_3]



	target = (True, [(-1,1), (4,6), (None,None), (None,None), (-1,1), (4,6), (None,None), (None,None)])

	initial_size = 0.3
	center = [-2,-4,0,0,2,-4,0,0]
	num_steps = 10

	u_dim = 4
	avoid_dynamic = None

	safe_rec = None
	# 78 iterations for now
	Theta = (True, [(-2.1, -1.9), (-4.1, -3.9), (0, 0), (0, 0), (1.9, 2.1), (-4.1, -3.9), (0, 0), (0, 0)])

	return initial_size, center, A, B, u_space, target, avoid_list, num_steps, u_dim, avoid_dynamic, Theta, safe_rec