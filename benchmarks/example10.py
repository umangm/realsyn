#10 car platoon
def name():
	return '10-car platoon'

def problem():
	A = [
	[1,0.1, 0,0,   0,0,   0,0,   0,0,   0,0,   0,0,  0,0,   0,0,   0,0],
	[0,1,   0,0,   0,0,   0,0,   0,0,   0,0,   0,0,  0,0,   0,0,   0,0],
	[0,0,   1,0.1, 0,0,   0,0,   0,0,   0,0,   0,0,  0,0,   0,0,   0,0],
	[0,0,   0,1,   0,0,   0,0,   0,0,   0,0,   0,0,  0,0,   0,0,   0,0],
	[0,0,   0,0,   1,0.1, 0,0,   0,0,   0,0,   0,0,  0,0,   0,0,   0,0],
	[0,0,   0,0,   0,1,   0,0,   0,0,   0,0,   0,0,  0,0,   0,0,   0,0],
	[0,0,   0,0,   0,0,   1,0.1, 0,0,   0,0,   0,0,  0,0,   0,0,   0,0],
	[0,0,   0,0,   0,0,   0,1,   0,0,   0,0,   0,0,  0,0,   0,0,   0,0],
	[0,0,   0,0,   0,0,   0,0,   1,0.1, 0,0,   0,0,  0,0,   0,0,   0,0],
	[0,0,   0,0,   0,0,   0,0,   0,1,   0,0,   0,0,  0,0,   0,0,   0,0],
	[0,0,   0,0,   0,0,   0,0,   0,0,   1,0.1, 0,0,  0,0,   0,0,   0,0],
	[0,0,   0,0,   0,0,   0,0,   0,0,   0,1,   0,0,  0,0,   0,0,   0,0],
	[0,0,   0,0,   0,0,   0,0,   0,0,   0,0,   1,0.1,0,0,   0,0,   0,0],
	[0,0,   0,0,   0,0,   0,0,   0,0,   0,0,   0,1,  0,0,   0,0,   0,0],
	[0,0,   0,0,   0,0,   0,0,   0,0,   0,0,   0,0,  1,0.1, 0,0,   0,0],
	[0,0,   0,0,   0,0,   0,0,   0,0,   0,0,   0,0,  0,1,   0,0,   0,0],
	[0,0,   0,0,   0,0,   0,0,   0,0,   0,0,   0,0,  0,0,   1,0.1, 0,0],
	[0,0,   0,0,   0,0,   0,0,   0,0,   0,0,   0,0,  0,0,   0,1,   0,0],
	[0,0,   0,0,   0,0,   0,0,   0,0,   0,0,   0,0,  0,0,   0,0,   1,0.1],
	[0,0,   0,0,   0,0,   0,0,   0,0,   0,0,   0,0,  0,0,   0,0,   0,1]
	]
	B = [
	[0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
	[0.1, 0,   0,   0,   0,   0,   0,   0,   0,   0],
	[0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
	[0.1, -0.1,0,   0,   0,   0,   0,   0,   0,   0],
	[0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
	[0,   0.1,-0.1, 0,   0,   0,   0,   0,   0,   0],
	[0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
	[0,   0,  0.1, -0.1, 0,   0,   0,   0,   0,   0],
	[0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
	[0,   0,   0,   0.1,-0.1, 0,   0,   0,   0,   0],
	[0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
	[0,   0,   0,   0,   0.1,-0.1, 0,   0,   0,   0],
	[0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
	[0,   0,   0,   0,   0,  0.1, -0.1, 0,   0,   0],
	[0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
	[0,   0,   0,   0,   0,   0, 0.1,-0.1,   0,   0],
	[0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
	[0,   0,   0,   0,   0,   0,   0, 0.1,-0.1,   0],
	[0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
	[0,   0,   0,   0,   0,   0,   0,   0, 0.1,-0.1],
	]

	u_range = 10
	u_space = (True, [(-u_range, u_range) for i in range(10)])


	avoid_1 = (True, [(None,None), (None,None), (None, 0),     (None, None), (None, None), (None, None), (None, None), (None, None), 
		              (None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None),
		              (None,None), (None,None), (None, None),  (None, None)] )

	avoid_2 = (True, [(None,None), (None,None), (None, None),  (None, None), (None, 0),    (None, None), (None, None), (None, None), 
		              (None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None),
		              (None,None), (None,None), (None, None),  (None, None)] )

	avoid_3 = (True, [(None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, 0),    (None, None),
		              (None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None),
		              (None,None), (None,None), (None, None),  (None, None)] )

	avoid_4 = (True, [(None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None),
		              (None,0),    (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None),
		              (None,None), (None,None), (None, None),  (None, None)] )

	avoid_5 = (True, [(None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None),
		              (None,None), (None,None), (None, 0),     (None, None), (None, None), (None, None), (None, None), (None, None),
		              (None,None), (None,None), (None, None),  (None, None)] )

	avoid_6 = (True, [(None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None),
		              (None,None), (None,None), (None, None),  (None, None), (None, 0),    (None, None), (None, None), (None, None),
		              (None,None), (None,None), (None, None),  (None, None)] )

	avoid_7 = (True, [(None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None),
		              (None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, 0),    (None, None),
		              (None,None), (None,None), (None, None),  (None, None)] )

	avoid_8 = (True, [(None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None),
		              (None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None),
		              (None,0),    (None,None), (None, None),  (None, None)] )

	avoid_9 = (True, [(None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, None), (None, None),
		              (None,None), (None,None), (None, None),  (None, None), (None, None), (None, None), (None, 0),    (None, None),
		              (None,None), (None,None), (None, 0),     (None, None)] )

	avoid_list = [avoid_1, avoid_2, avoid_3, avoid_4, avoid_5, avoid_6, avoid_7, avoid_8, avoid_9]

	target = (True, [(20, 22), (21, 23), (1, 2), (-1, 1), (1, 2), (-1, 1), (1, 2), (-1, 1), 
		             (1, 2),    (-1, 1), (1, 2), (-1, 1), (1, 2), (-1, 1), (1, 2), (-1, 1),
		             (1, 2),    (-1, 1), (1, 2), (-1, 1)])

	initial_size = 0.3
	center = [0,20,1,0,1,0,1,0,
			  1,0,1,0, 1,0,1,0,
			  1,0,1,0]

	num_steps = 10

	u_dim = 10

	avoid_dynamic = None

	Theta = (True, [(c-0.05, c + 0.05) for c in center])
	safe_rec = None

	return initial_size, center, A, B, u_space, target, avoid_list, num_steps, u_dim, avoid_dynamic, Theta, safe_rec
