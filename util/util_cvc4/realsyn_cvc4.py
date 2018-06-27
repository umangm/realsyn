import sys
sys.path.append("..")
from cntrl.Kfunctions import *
from synth_set import *
import math
from CVC4 import ExprManager, SmtEngine, SExpr, Rational
import CVC4

multiplicative_factor_for_radius = 0.95
max_decrease_steps = 100
max_num_iters = 200
print_detail = False
# option_center = True

def get_controller_cvc4(Theta, initial_size, A, B, u_dim, u_poly, target, avoid_list, avoid_list_dynamic, safe, num_steps, Q_multiplier):
	#set safe to be None if you want to run the avoid_list version. Else set avoid_list to be None

	P, radius_dim, _, lam, G = get_overapproximate_rectangles(A, B, Q_multiplier, num_steps)
	radius_list = radius_without_r0(P, radius_dim, num_steps, lam)
	K = G*(-1)
	
	x_dim = len(radius_list[0])
	sqrt_dim_inverse = 10000.0/(math.floor(math.sqrt(x_dim*100000000.0)))

	em = ExprManager()
	s = SmtEngine(em)
	s.setOption("produce-models", SExpr("true"))
	real_type = em.realType()

	x = [[em.mkVar("x_ref_%s[%s]" %(i, j+1), real_type) for j in range(x_dim)] for i in range(num_steps+1)]
	u = [[em.mkVar("u_ref_%s[%s]" %(i, j+1), real_type) for j in range(u_dim)] for i in range(num_steps)]
	r = em.mkVar("r0", real_type)
	initial_rectangle = []
	for i in range(x_dim):
		rl_mult_r = em.mkExpr(CVC4.MULT, get_cvc4_const(em, radius_list[0][i]), r)
		lo = em.mkExpr(CVC4.MINUS, x[0][i], rl_mult_r)
		hi = em.mkExpr(CVC4.PLUS, x[0][i], rl_mult_r)
		initial_rectangle.append((lo, hi))

	if print_detail:
		print("Adding constraints ... ")
	if safe is None:
		add_constraints(s, em, x, u, r, Theta, radius_list, x_dim, A, u_dim, B, u_poly, target, avoid_list, avoid_list_dynamic, initial_rectangle, num_steps)
	else:
		add_constraints_safety(s, em, x, u, r, Theta, radius_list, x_dim, A, u_dim, B, u_poly, target, safe, initial_rectangle, num_steps)
	
	if print_detail:
		print("Done adding main constraints ... ")

	first_trajectory_found = False
	s.push()
	if print_detail:
		print("Now adding Theta constraints ... ")
	add_Theta_constraint(s, em, Theta, x[0], True)
	s.push()
	if print_detail:
		print("Done adding Theta constraints ... ")
		print("Now adding radius constraints ... ")
	add_radius_constraint(s, em, r, get_cvc4_const(em, initial_size))

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

		s_check = s.checkSat()
		if print_detail:
			print("checked")
		if (s_check.isSat() == 1):
			# trajectory_radius_controller_list = [[]]
			trajectory = [[ s.getValue(x[i][j]).getConstRational().getDouble() for j in range(x_dim)] for i in range(num_steps+1)]
			controller = [[ s.getValue(u[i][j]).getConstRational().getDouble() for j in range(u_dim)] for i in range(num_steps)]

			rad = s.getValue(r).getConstRational().getDouble()			
			init_point = trajectory[0]
			init_radius = [r_i*rad*sqrt_dim_inverse for r_i in radius_list[0]]
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
				add_Theta_constraint(s, em, Theta, x[0], False)
			else:
				s.pop()

			add_cover_constraint(s, em, (True, cover), x[0], initial_rectangle)
			s.push()
			add_radius_constraint(s, em, r, get_cvc4_const(em, initial_size))

		else :
			if print_detail:
				print("Fails for:", initial_size)
			initial_size = initial_size * multiplicative_factor_for_radius
			number_of_steps_initial_size_has_been_halved = number_of_steps_initial_size_has_been_halved + 1
			s.pop()
			s.push()
			add_radius_constraint(s, em, r, get_cvc4_const(em, initial_size))

	print("Number of iterations: " + str(num_iters))
	return (K, trajectory_radius_controller_list, covered_list, num_iters)