#8 car platoon
def name():
	return '8-car platoon'

def problem():
	# System dynamics: x1' = x2, x2' = u1, x3' = x4, x4' = u1-u2, x5' = x6, x6' = u2-u3, x7' = x8, x8' = u3-u4
	# Discretize: x1 = x1 + x2, x2 = x2 + u1, x3 = x3 +x4, x4 = x4 + u1 - u2, x5 = x5 + x6, 
	# x6 = x6 + u2 - u3, x7 = x7 + x8, x8 = x8 + u3-u4

	A = [
	[1,0.1, 0,0,   0,0, 0,0,   0,0, 0,0, 0,0, 0,0],
	[0,1,   0,0,   0,0, 0,0,   0,0, 0,0, 0,0, 0,0],
	[0,0,   1,0.1, 0,0, 0,0,   0,0, 0,0, 0,0, 0,0],
	[0,0,   0,1,   0,0, 0,0,   0,0, 0,0, 0,0, 0,0],
	[0,0,   0,0,   1,0.1, 0,0, 0,0, 0,0, 0,0, 0,0],
	[0,0,   0,0,   0,1,   0,0, 0,0, 0,0, 0,0, 0,0],
	[0,0, 0,0,   0,0,   1,0.1, 0,0, 0,0, 0,0, 0,0],
	[0,0, 0,0,   0,0,   0,1,   0,0, 0,0, 0,0, 0,0],
	[0,0, 0,0,   0,0,   0,0, 1,0.1, 0,0, 0,0, 0,0],
	[0,0, 0,0,   0,0,   0,0, 0,1,   0,0, 0,0, 0,0],
	[0,0, 0,0,   0,0,   0,0, 0,0, 1,0.1, 0,0, 0,0],
	[0,0, 0,0,   0,0,   0,0, 0,0, 0,1,   0,0, 0,0],
	[0,0, 0,0,   0,0,   0,0, 0,0, 0,0,  1,0.1,0,0],
	[0,0, 0,0,   0,0,   0,0, 0,0, 0,0,  0,1,  0,0],
	[0,0, 0,0,   0,0,   0,0, 0,0, 0,0,  0,0,1,0.1],
	[0,0, 0,0,   0,0,   0,0, 0,0, 0,0,  0,0,  0,1]
	]
	B = [
	[0,   0,   0,   0,   0,   0,   0,   0],
	[0.1, 0,   0,   0,   0,   0,   0,   0],
	[0,   0,   0,   0,   0,   0,   0,   0],
	[0.1, -0.1,0,   0,   0,   0,   0,   0],
	[0,   0,   0,   0,   0,   0,   0,   0],
	[0,   0.1,-0.1, 0,   0,   0,   0,   0],
	[0,   0,   0,   0,   0,   0,   0,   0],
	[0,   0,  0.1, -0.1, 0,   0,   0,   0],
	[0,   0,   0,   0,   0,   0,   0,   0],
	[0,   0,   0,   0.1,-0.1, 0,   0,   0],
	[0,   0,   0,   0,   0,   0,   0,   0],
	[0,   0,   0,   0,   0.1,-0.1, 0,   0],
	[0,   0,   0,   0,   0,   0,   0,   0],
	[0,   0,   0,   0,   0,  0.1, -0.1, 0],
	[0,   0,   0,   0,   0,   0,   0,   0],
	[0,   0,   0,   0,   0,   0, 0.1,-0.1],
	]

	u_range = 10
	u_space = (True, [(-u_range, u_range) for i in range(8)])


	avoid_1 = (True, [(None,None), (None,None), (None, 0),     (None, None), (None, None), (None, None), (None, None), (None, None), 
		              (None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None)] )

	avoid_2 = (True, [(None,None), (None,None), (None, None),  (None, None), (None, 0),    (None, None), (None, None), (None, None), 
		              (None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None)] )

	avoid_3 = (True, [(None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, 0),    (None, None),
		              (None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None)] )

	avoid_5 = (True, [(None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None),
		              (None,0),    (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None)] )

	avoid_6 = (True, [(None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None),
		              (None,None), (None,None), (None, 0),     (None, None), (None, None), (None, None), (None, None), (None, None)] )

	avoid_7 = (True, [(None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None),
		              (None,None), (None,None), (None, None),  (None, None), (None, 0),    (None, None), (None, None), (None, None)] )

	avoid_8 = (True, [(None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None),
		              (None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, 0),    (None, None)] )

	avoid_list = [avoid_1, avoid_2, avoid_3, avoid_5, avoid_6, avoid_7, avoid_8]

	target = (True, [(20, 22), (21, 23), (1, 2), (-1, 1), (1, 2), (-1, 1), (1, 2), (-1, 1), 
		             (1, 2),    (-1, 1), (1, 2), (-1, 1), (1, 2), (-1, 1), (1, 2), (-1, 1)])

	initial_size = 0.3
	center = [0,20,1,0,1,0,1,0,
			  1,0,1,0, 1,0,1,0]

	num_steps = 10
	u_dim = 8

	avoid_dynamic = None

	Theta = (True, [(c-0.07, c + 0.07) for c in center])
	safe_rec = None

	return initial_size, center, A, B, u_space, target, avoid_list, num_steps, u_dim, avoid_dynamic, Theta, safe_rec