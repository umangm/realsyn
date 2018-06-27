import os.path
import numpy as np
import scipy.linalg as la

#building
def name():
	return 'building'

def problem():

	HERE = os.path.dirname(os.path.abspath(__file__))
	filename_A = HERE+"/aux-matrices/building_A.txt"
	filename_B = HERE+"/aux-matrices/building_B.txt"

	# First read the continuous system from the txt file.
	with open(filename_A, 'r') as f:
	    A_conti = []
	    for line in f: # read rest of lines
	        A_conti.append([float(x) for x in line.split()])
	with open(filename_B, 'r') as f:
	    B_conti = []
	    for line in f: # read rest of lines
	        B_conti.append([float(x) for x in line.split()])
	
	time_step = 0.1
	dim = len(A_conti[0])

	# Discretize the system using matrix exponential

	A_conti = np.array(A_conti)
	B_conti = np.array(B_conti)

	A = la.expm(A_conti * time_step)
	B = np.dot( np.dot(np.linalg.inv(A_conti), (A - np.eye(dim))), B_conti)

	u_space = (True, [(0.9, 1.0)])

	reach_bound = 100.0

	safe_rec = (True,[(None, None) for i in range(24)] + [(None, 0.006)] + [(None, None) for i in range(23)] )

	avoid_list = None

	target = safe_rec

	initial_size = 0.0001
	center = [0.00025 for i in range(10)] + [0 for i in range(38)]
	num_steps = 10
	u_dim = 1

	avoid_dynamic = None

	Theta = (True, [(0.0002 - initial_size/10, 0.0002 + initial_size/10 ) for i in range(10)] + [(0, 0) for i in range(14)] + [(0.0 - initial_size/10, 0.0 + initial_size/10)] + [(0, 0) for i in range(23)] )


	num_steps = 10

	# P, radius_dim, num_steps, lam = get_overapproximate_rectangles(A, B, 1, num_steps)
	return initial_size, center, A, B, u_space, target, avoid_list, num_steps,u_dim, avoid_dynamic, Theta, safe_rec
