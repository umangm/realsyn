from math import sqrt

#satellite
def name():
	return 'satellite'

def problem():
	A = [[2,-1],[1,0]] 
	B = [[2],[0]] 
	x_dim = len(A[0])
	u_dim = len(B[0])
	u_bound = 10
	u_space = (True, [(-u_bound, u_bound) for i in range(u_dim)])
	reach_bound = 1.5
	safe_rec = (True,[(-reach_bound, reach_bound) for i in range(x_dim)])
	target = safe_rec
	initial_size = 1.0 * sqrt(x_dim)
	center = [0,0,0]
	num_steps = 10
	Theta = avoid_6 = (True, [(-1.0, 1.0) for i in range(x_dim)] )
	avoid_list = None
	avoid_dynamic = None
	return initial_size, center, A, B, u_space, target, avoid_list, num_steps,u_dim, avoid_dynamic, Theta, safe_rec
