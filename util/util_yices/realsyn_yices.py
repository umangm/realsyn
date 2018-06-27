import sys
sys.path.append("..")
from cntrl.Kfunctions import *
from synth_set import *
import math
from yices import *
from ctypes import ( c_int32 )
from ctypes import ( c_double )


multiplicative_factor_for_radius = 0.95
max_decrease_steps = 100
max_num_iters = 200
print_detail = False
# option_center = True

def get_controller_yices(Theta, initial_size, A, B, u_dim, u_poly, target, avoid_list, avoid_list_dynamic, safe, num_steps, Q_multiplier):
	#set safe to be None if you want to run the avoid_list version. Else set avoid_list to be None
	
	P, radius_dim, _, lam, G = get_overapproximate_rectangles(A, B, Q_multiplier, num_steps)
	radius_list = radius_without_r0(P, radius_dim, num_steps, lam)
	x_dim = len(radius_list[0])
	sqrt_dim_inverse = 10000.0/(math.floor(math.sqrt(x_dim*100000000.0)))
	K = G*(-1)


	yices_init()
	real_t = yices_real_type()
	config = yices_new_config()
	yices_default_config_for_logic(config, "QF_LRA")
	yices_set_config(config, "mode", "push-pop")
	context = yices_new_context(config)

	x = [[yices_new_uninterpreted_term(real_t) for j in range(x_dim)] for i in range(num_steps+1)]
	for i in range(num_steps+1):
		for j in range(x_dim):
			yices_set_term_name(x[i][j], "x_ref_%s_%s" %(i, j+1))

	u = [[yices_new_uninterpreted_term(real_t) for j in range(u_dim)] for i in range(num_steps)]
	for i in range(num_steps):
		for j in range(u_dim):
			yices_set_term_name(u[i][j], "u_ref_%s_%s" %(i, j+1))

	r = yices_new_uninterpreted_term(real_t)
	yices_set_term_name(r, "r0")

	initial_rectangle = []
	for i in range(x_dim):
		rl_mult_r = yices_mul(get_yices_const(radius_list[0][i]), r)
		lo = yices_sub(x[0][i], rl_mult_r)
		hi = yices_add(x[0][i], rl_mult_r)
		initial_rectangle.append((lo, hi))

	if print_detail:
		print("Adding constraints ... ")
	if safe is None:
		f = add_constraints(x, u, r, Theta, radius_list, x_dim, A, u_dim, B, u_poly, target, avoid_list, avoid_list_dynamic, initial_rectangle, num_steps)
		yices_assert_formula(context, f)
	else:
		if print_detail:
			print("safety only")
		f = add_constraints_safety(x, u, r, Theta, radius_list, x_dim, A, u_dim, B, u_poly, target, safe, initial_rectangle, num_steps)
		yices_assert_formula(context, f)
	if print_detail:
		print("Done adding main constraints ... ")
	
	first_trajectory_found = False
	yices_push(context)

	if print_detail:
		print("Now adding Theta constraints ... ")
	f = add_Theta_constraint(Theta, x[0], True)
	yices_assert_formula(context, f)
	yices_push(context)

	if print_detail:
		print("Done adding Theta constraints ... ")
		print("Now adding radius constraints ... ")
	f = add_radius_constraint(r, get_yices_const(initial_size))
	yices_assert_formula(context, f)

	if print_detail:
		print("Done adding radius constraints ... ")

	Theta_has_been_covered = False
	number_of_steps_initial_size_has_been_halved = 0
	num_iters = 0
	covered_list = []
	trajectory_radius_controller_list = [] #List of tuples of the form (trajectory, radius_list)

	if print_detail:
		print("Starting iterations")

	while((not Theta_has_been_covered) and number_of_steps_initial_size_has_been_halved < max_decrease_steps and num_iters < max_num_iters):
		num_iters = num_iters + 1

		s_check = yices_check_context(context, None)
		if print_detail:
			print("checked")
		if (s_check == STATUS_SAT):
			model = yices_get_model(context, 1)
			val = c_double()

			trajectory = []
			for i in range(num_steps+1):
				trajectory.append([])
				for j in range(x_dim):
					yices_get_double_value(model, x[i][j], val)
					trajectory[i].append(val.value)

			controller = []
			for i in range(num_steps):
				controller.append([])
				for j in range(u_dim):
					yices_get_double_value(model, u[i][j], val)
					controller[i].append(val.value)
			
			yices_get_double_value(model, r, val)
			rad = val.value
			
			yices_free_model(model)

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

			if(Theta_has_been_covered):
				break

			if print_detail:
				print("Found trajectory from:", trajectory[0], "with radius = ", init_radius[0])

			if not first_trajectory_found :
				first_trajectory_found = True
				yices_pop(context)
				yices_pop(context)
				f = add_Theta_constraint(Theta, x[0], False)
				yices_assert_formula(context, f)
			else:
				yices_pop(context)

			f = add_cover_constraint((True, cover), x[0], initial_rectangle)

			yices_assert_formula(context, f)

			yices_push(context)
			f = add_radius_constraint(r, get_yices_const(initial_size))
			yices_assert_formula(context, f)

		else :
			if print_detail:
				print("Fails for:", initial_size)
			initial_size = initial_size * multiplicative_factor_for_radius
			number_of_steps_initial_size_has_been_halved = number_of_steps_initial_size_has_been_halved + 1
			yices_pop(context)
			yices_push(context)
			f = add_radius_constraint(r, get_yices_const(initial_size))
			yices_assert_formula(context, f)

	yices_free_context(context)
	yices_free_config(config)
	yices_exit()

	print("Number of iterations: " + str(num_iters))
	return (K, trajectory_radius_controller_list, covered_list, num_iters)