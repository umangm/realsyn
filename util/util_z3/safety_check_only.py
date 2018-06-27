import sys
sys.path.append("..")
from cntrl.Kfunctions import *
from synth_set import *
import math
from z3 import *

def get_safety_constraint_hyperrectangle(interval_list, safety_set):
	#interval_list = [(lo_1, hi_1), (lo_2, hi_2), ..., (lo_k, hi_k)] represents a polytope, with k = dimension of the state space.
	assert safety_set[0], "The safety set/reachset should be a hyper-rectangle!"
	return get_rect_rect_containment_constraint(interval_list, safety_set[1])


def get_controller_from_set_safety_only(center, radius_list, x_dim, A, u_dim, B, u_space, target_poly, safety_set, num_steps):
	#center, radius_list[0] represent the initial set
	#Radius_list = [lst_1, lst_2, ..., lst_m], where m= num_steps, and each lst_i = [r1, ..., r_k], k = x_dim is the per-dimension radius at the i'th step
	#A is a constant square matrix of dimension x_dim \times x_dim
	#u_dim is the dimension of the input space
	#B is the feedback matrix of dimension x_dim\times u_dim
	#u_poly = (u_mat, u_vec) represents the space of inputs. That is, we allow any u that satisfies u_mat\times u + u_vec <= 0
	#target_poly = (target_mat, target_vec) is the target polytope
	#avoid_list is a list [(flag1, poly1), (flag2, poly2) ...  (flagk, polyk)], where flagi = True means rectangle, o/w general polytope. if flagi = True, thn polyi = list of x_dim pairs (hi, low). O/w it is (Ai, bi).

	x = [[Real("x_ref_%s[%s]" %(i, j+1)) for j in range(x_dim)] for i in range(num_steps+1)]
	u = [[Real("u_ref_%s[%s]" %(i, j+1)) for j in range(u_dim)] for i in range(num_steps)]	
	s = Solver()

	initial_interval_list = [(center[i]-radius_list[0][i], center[i]+radius_list[0][i]) for i in range(x_dim)]
	x_0_lst = []
	for i in range(x_dim):
		x_0_lst.append(x[0][i] == center[i])

	s.add(And(x_0_lst))
	s.add(get_safety_constraint_hyperrectangle(initial_interval_list, safety_set))

	for i in range(num_steps):
		u_i_constraint = get_point_membership_constraint(u[i], u_space) #get_poly_constraint(u[i], u_mat, u_vec, u_mat_dim, u_dim)
		next_x_constraint = get_next_constraint_point(x[i], u[i], A, B, x_dim, u_dim, x[i+1])
		reach_interval_list = [(x[i+1][j] - radius_list[i+1][j], x[i+1][j] + radius_list[i+1][j]) for j in range(x_dim)]
		safety_constraint = get_safety_constraint_hyperrectangle(reach_interval_list, safety_set)

		s.add(u_i_constraint)
		s.add(next_x_constraint)
		s.add(safety_constraint)

	reach_constraint = get_safety_constraint_hyperrectangle(reach_interval_list, target_poly)
	s.add(reach_constraint) 

	#print("start z3")

	covered_list = []
	trajectory_radius_controller_list = [] #List of tuples of the form (trajectory, radius_list, controller)

	if(s.check() == sat):
		m = s.model()
		trajectory = [[m[x[i][j]].as_fraction() for j in range(x_dim)] for i in range(num_steps+1)]
		controller = [[m[u[i][j]].as_fraction() for j in range(u_dim)] for i in range(num_steps)]
		cover = initial_interval_list
		covered_list.append((True,cover))

		trajectory_radius_controller_list.append((trajectory, radius_list, controller))

	elif(s.check() == unsat):
		print("Z3 said UNSAT !")

	return (trajectory_radius_controller_list, covered_list, 1)

def get_controller_nonincremental_z3(Theta, initial_size, A, B, u_dim, u_poly, target, avoid_list, avoid_list_dynamic, safe, num_steps, Q_multiplier):
	#A and B specify the dynamics
	#target = (target_mat, target_vec) is the target polytope
	#avoid_list = [avoid_1, ..., avoid_n] is a list of polyhedra avoid_i = (avoid_mat_i, avoid_vec_i) that are unsafe

	(Theta_flag, Theta_desc) = Theta
	center = [(hi+lo)/2 for (lo, hi) in Theta_desc]

	P, radius_dim, num_steps, lam, G = get_overapproximate_rectangles(A, B, 10, num_steps)
	K = G*(-1)
	radius_list_original = radius_without_r0(P, radius_dim, num_steps, lam)
	radius_list = [[radius_per_dim * initial_size for radius_per_dim in radius] for radius in radius_list_original]

	x_dim = len(radius_list[0])
	(trajectory_radius_controller_list, covered_list, num_iters) =  get_controller_from_set_safety_only(center, radius_list, x_dim, A, u_dim, B, u_poly, target, safe, num_steps)
	return (K, trajectory_radius_controller_list, covered_list, num_iters)