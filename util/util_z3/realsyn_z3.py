import sys
sys.path.append("..")
from cntrl.Kfunctions import *
from synth_set import *
import math
from z3 import *

multiplicative_factor_for_radius = 0.95
max_decrease_steps = 100
max_num_iters = 200
print_detail = False
# option_center = True

def get_controller_z3(Theta, initial_size, A, B, u_dim, u_poly, target, avoid_list, avoid_list_dynamic, safe, num_steps, Q_multiplier):
	#set safe to be None if you want to run the avoid_list version. Else set avoid_list to be None
	
	P, radius_dim, _, lam, G = get_overapproximate_rectangles(A, B, Q_multiplier, num_steps)
	radius_list = radius_without_r0(P, radius_dim, num_steps, lam)
	K = G*(-1)
	
	x_dim = len(radius_list[0])
	sqrt_dim_inverse = 10000.0/(math.floor(math.sqrt(x_dim*100000000.0)))

	x = [[Real("x_ref_%s[%s]" %(i, j+1)) for j in range(x_dim)] for i in range(num_steps+1)]
	u = [[Real("u_ref_%s[%s]" %(i, j+1)) for j in range(u_dim)] for i in range(num_steps)]
	r = Real("r0")
	initial_rectangle = [(x[0][i]-radius_list[0][i]*r, x[0][i]+radius_list[0][i]*r) for i in range(x_dim)]

	s = Solver()
	if print_detail:
		print("Adding constraints ... ")
	if safe is None:
		add_constraints(s, x, u, r, Theta, radius_list, x_dim, A, u_dim, B, u_poly, target, avoid_list, avoid_list_dynamic, initial_rectangle, num_steps)
	else:
		add_constraints_safety(s, x, u, r, Theta, radius_list, x_dim, A, u_dim, B, u_poly, target, safe, initial_rectangle, num_steps)
	
	if print_detail:
		print("Done adding main constraints ... ")
	

	first_trajectory_found = False
	s.push()
	if print_detail:
		print("Now adding Theta constraints ... ")
	add_Theta_constraint(s, Theta, x[0], True)
	s.push()
	if print_detail:
		print("Done adding Theta constraints ... ")
		print("Now adding radius constraints ... ")
	add_radius_constraint(r, s, initial_size)

	if print_detail:
		print("Done adding radius constraints ... ")

	Theta_has_been_covered = False
	number_of_steps_initial_size_has_been_halved = 0
	num_iters = 0
	covered_list = []
	trajectory_radius_controller_list = [] #List of tuples of the form (trajectory, radius_list, controller)

	if print_detail:
		print("Starting iterations")

	while((not Theta_has_been_covered) and number_of_steps_initial_size_has_been_halved < max_decrease_steps and num_iters < max_num_iters):
		num_iters = num_iters + 1

		s_check = s.check()
		if print_detail:
			print("checked")
		if (s_check == sat):
			m = s.model()
			# print("model=", m)
			trajectory = [[ (m[x[i][j]].numerator_as_long())*1.0/(m[x[i][j]].denominator_as_long()) for j in range(x_dim)] for i in range(num_steps+1)]
			controller = [[ (m[u[i][j]].numerator_as_long())*1.0/(m[u[i][j]].denominator_as_long()) for j in range(u_dim)] for i in range(num_steps)]
			rad = (m[r].numerator_as_long())*1.0/(m[r].denominator_as_long())
			init_point = trajectory[0]
			init_radius = [r_i*rad*sqrt_dim_inverse for r_i in radius_list[0]] #is the sqrt_2 needed ?
			cover = []
			for i in range(len(init_point)):
				x_i = init_point[i]
				r_i = init_radius[i]
				cover.append((x_i-r_i, x_i+r_i))
			covered_list.append((True,cover))
			Theta_has_been_covered = check_covered(x_dim, Theta, covered_list)
			trajectory_radius_controller_list.append((trajectory, [[rad * rad_dim for rad_dim in rad_step] for  rad_step in radius_list], controller))

			if print_detail:
				print("Found trajectory from:", trajectory[0], "with radius = ", init_radius[0])

			if not first_trajectory_found :
				first_trajectory_found = True
				s.pop()
				s.pop()
				add_Theta_constraint(s, Theta, x[0], False)
			else:
				s.pop()

			add_cover_constraint((True, cover), x[0], s, initial_rectangle)
			s.push()
			add_radius_constraint(r, s, initial_size)

		elif(s_check == unsat):
			if print_detail:
				print("Fails for:", initial_size)
			initial_size = initial_size * multiplicative_factor_for_radius
			number_of_steps_initial_size_has_been_halved = number_of_steps_initial_size_has_been_halved + 1
			s.pop()
			s.push()
			add_radius_constraint(r, s, initial_size)

		else: 
			if print_detail:
				print("z3 returned an unknown result")

	print("Number of iterations: " + str(num_iters))
	return (K, trajectory_radius_controller_list, covered_list, num_iters)