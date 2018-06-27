import os.path
import sys
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

def get_q_multiplier(n):
	if n in [8, 9, 10]:
		return 900
	elif n in [20, 21]:
		return 100
	else:
		return 1

def get_benchmark_params(n):
	mod = importlib.import_module("example" + str(n))
	_, _, A, _, _, _, _, _,u_dim, _, _, _ =  mod.problem()

	return (len(A), u_dim, mod.name())

def get_benchmark(n):
	mod = importlib.import_module("example" + str(n))
	return mod.problem()

