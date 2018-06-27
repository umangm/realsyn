from subprocess import call
import util.cmd_opts as cmd_opts

import os.path
import importlib
import time

from benchmarks.benchmarks import get_benchmark_params
from realsyn import run_realsyn
from util.util_table import get_csv_table

HERE = os.path.dirname(os.path.abspath(__file__))

timeout_combinations = [(22, 'z3'), (24, 'z3'), (3, 'cvc4'), (23, 'cvc4'), (22, 'yices')]

def runall(solvers, run_timeout_combinations):
	table = dict()
	
	for benchmark in range(1,25):

		table_benchmark = dict()

		(n, m, name) = get_benchmark_params(benchmark)
		table_benchmark['n'] = n
		table_benchmark['m'] = m
		table_benchmark['model'] = name

		for solver in solvers:
			if ((benchmark, solver) in timeout_combinations) and not run_timeout_combinations:
				print("Benchmark #" + str(benchmark) + " may timeout on the solver " + solver + ". Enable 'run_timeout_combinations' flag to run these")
			
			else:
				print("============Running benchmark " + str(benchmark) + " with solver " + solver + "===============")
				t0 = time.time()
				# command = ['python', HERE + '/' + 'realsyn.py', '-s', solver, '-b', str(benchmark)]
				# call(command)
				(_, _, _, num_iters) = run_realsyn(solver, benchmark, False)
				t1 = time.time()

				table_benchmark[solver + '-iter'] = num_iters
				table_benchmark[solver + '-time'] = t1-t0
				print("time = " + str(t1-t0) + " seconds")
				print("=====================================================================\n")

		table[benchmark] = table_benchmark

	######### Now run the last three benchmarks with z3's non-incremental engine ##########

	solver = 'z3'
	if solver in solvers:
		for benchmark in range(22,25):
			print("============Running benchmark " + str(benchmark) + " with non-incremental-solver " + solver + "===============")
			t0 = time.time()
			# command = ['python', HERE + '/' + 'realsyn.py', '-s', solver, '-b', str(benchmark), '-n']
			# call(command)
			(_, _, _, num_iters) =  run_realsyn(solver, benchmark, True)
			t1 = time.time()

			table[benchmark]['z3-iter-n'] = num_iters
			table[benchmark]['z3-time-n'] = t1-t0
			print("=====================================================================\n")
	
	return table

def main():
	(solver, gen_table, run_timeout_combinations) = cmd_opts.get_cmd_opts_runall()
	solvers = ['z3', 'yices', 'cvc4']
	if not(solver == 'all'):
		solvers = [solver]

	print("")
	table = runall(solvers, run_timeout_combinations)
	if gen_table:
		print("\n################### Table ####################\n") 
		print(get_csv_table(table))
		print("\n##############################################\n")

if __name__ == "__main__":
	main()