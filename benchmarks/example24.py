import os.path
import numpy as np
import scipy.linalg as la

#pde
def name():
	return 'pde'

def problem():

	HERE = os.path.dirname(os.path.abspath(__file__))
	filename_A = HERE+"/aux-matrices/PDE_A.txt"
	filename_B = HERE+"/aux-matrices/PDE_B.txt"

	# First read the continuous system from the txt file.
	with open(filename_A, 'r') as f:
	    A_conti = []
	    for line in f: # read rest of lines
	        A_conti.append([float(x) for x in line.split(',')])
	with open(filename_B, 'r') as f:
	    B_conti = []
	    for line in f: # read rest of lines
	        B_conti.append([float(x) for x in line.split(',')])
	
	time_step = 0.1
	dim = len(A_conti[0])

	# Discretize the system using matrix exponential

	A_conti = np.array(A_conti)
	B_conti = np.array(B_conti)

	A = la.expm(A_conti * time_step)
	B = np.dot( np.dot(np.linalg.inv(A_conti), (A - np.eye(dim))), B_conti)

	u_space = (True, [(0.5, 1.0)])

	safe_rec = (True,[(-1, 1) for i in range(1)] + [(None, None) for i in range(83)] )

	avoid_list = None

	target = safe_rec

	initial_size = 0.01
	# center = [0.0 for i in range(64)] + [0.001 for i in range(16)] + [-0.001 for i in range(4)]
	center = None

	num_steps = 10
	u_dim = 1

	avoid_dynamic = None

	Theta = (True, [(0.0,0.0) for i in range(64)] + [(0.00, 0.001) for i in range(16)] + [(-0.001, 0.0) for i in range(4)] )

	return initial_size, center, A, B, u_space, target, avoid_list, num_steps,u_dim, avoid_dynamic, Theta, safe_rec

