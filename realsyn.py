from util.util_z3.realsyn_z3 import *
from util.util_z3.safety_check_only import get_controller_nonincremental_z3
from util.util_yices.realsyn_yices import *
# from util.util_cvc4.realsyn_cvc4 import *
from benchmarks.benchmarks import get_benchmark, get_q_multiplier
import time
import util.cmd_opts as cmd_opts

def pretty_print_controller(K, trajectory_radius_controller_list, covered_list):
	print('\n ############## Printing Controller ##############\n')
	print("K (common to all trjaectories) = " + str(K))
	# print(K)
	print("\nSub-controllers:\n")
	l = len(covered_list)
	for i in range(l):
		print('********* ' + str(i) + ' *********')
		(trajectory, _, controller) = trajectory_radius_controller_list[i]
		print('x_ref[0] = ' + str(trajectory[0]))
		print('\ncontroller (control input for each time-step) = ')
		steps = len(controller)
		for j in range(steps):
			print("Step# " + str(j) + ": " + str(controller[j]))
		print('\nSubset of Theta covered by this controller = ')
		cover = covered_list[i]
		(cvr_flag, cvr_desc) = cover
		print(('Rectangle: ' if cvr_flag else 'Polytope: ') + str(cvr_desc) )
		print('************************* \n')


def run_realsyn(solver, benchmark, nonincremental):
	
	K = None
	trajectory_radius_controller_list = []
	covered_list = []
	num_iters = None

	(initial_size, _, A, B, u_space, target, avoid_list, num_steps,u_dim, avoid_dynamic, Theta, safe_rec) = get_benchmark(benchmark)
	q_multiplier = get_q_multiplier(benchmark)

	if solver == 'z3':
		if (benchmark in [22, 23, 24] and nonincremental):
			(K, trajectory_radius_controller_list, covered_list, num_iters) = get_controller_nonincremental_z3(Theta, initial_size, A, B, u_dim, u_space, target, avoid_list, avoid_dynamic, safe_rec, num_steps, q_multiplier)
		else:
			(K, trajectory_radius_controller_list, covered_list, num_iters) = get_controller_z3(Theta, initial_size, A, B, u_dim, u_space, target, avoid_list, avoid_dynamic, safe_rec, num_steps, q_multiplier)
	elif solver == 'yices':
		(K, trajectory_radius_controller_list, covered_list, num_iters) = get_controller_yices(Theta, initial_size, A, B, u_dim, u_space, target, avoid_list, avoid_dynamic, safe_rec, num_steps, q_multiplier)
	elif solver == 'cvc4':
		(K, trajectory_radius_controller_list, covered_list, num_iters) = get_controller_cvc4(Theta, initial_size, A, B, u_dim, u_space, target, avoid_list, avoid_dynamic, safe_rec, num_steps, q_multiplier)

	return (K, trajectory_radius_controller_list, covered_list, num_iters)

def main():
	(solver, benchmark, printcontroller, nonincremental) = cmd_opts.get_cmd_opts()
	t0 = time.time()
	(K, trajectory_radius_controller_list, covered_list, num_iters) = run_realsyn(solver, benchmark, nonincremental)
	if printcontroller:
		pretty_print_controller(K, trajectory_radius_controller_list, covered_list)
	t1 = time.time()
	print("Time for benchmark #" + str(benchmark) + " is " + str(t1 - t0) + " seconds\n")	

if __name__ == "__main__":
	main()
