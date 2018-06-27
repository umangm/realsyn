from math import sqrt

#tape
def name():
	return 'tape'

def problem():
	A = [[5.5197e-17,-3.5503e-17,6.2468e-32],[2.7756e-17,0,0],[0,2.7756e-17,0]] 
	B = [[0.25],[0],[0]]  
	x_dim = len(A[0])
	u_dim = len(B[0])
	u_bound = 10
	u_space = (True, [(-u_bound, u_bound) for i in range(u_dim)])
	reach_bound = 3.0
	safe_rec = (True,[(-reach_bound, reach_bound) for i in range(x_dim)])
	target = safe_rec
	initial_size = 1.0 * sqrt(x_dim)
	center = [0,0,0]
	num_steps = 10
	Theta = avoid_6 = (True, [(-1.0, 1.0) for i in range(x_dim)] )
	avoid_list = None
	avoid_dynamic = None
	return initial_size, center, A, B, u_space, target, avoid_list, num_steps,u_dim, avoid_dynamic, Theta, safe_rec
