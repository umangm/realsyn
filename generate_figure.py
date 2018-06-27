from subprocess import call
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import os.path
import sys
import importlib

from util.util_yices.realsyn_yices import *
from benchmarks.benchmarks import get_benchmark



# HERE = os.path.dirname(os.path.abspath(__file__))

# timeout_combinations = [(22, 'z3'), (24, 'z3'), (3, 'cvc4'), (23, 'cvc4'), (22, 'yices')]
# run_timeout_combinations = False

def get_plotter_things(x_range, y_range):
	corner = (x_range[0], y_range[0])
	width = x_range[1] - x_range[0]
	height = y_range[1] - y_range[0]
	return corner, width, height

def plotter_room(trajectory_radius_controller_list, avoid_list, target, covered_list, Theta):
	fig = plt.figure()

	SMALL_SIZE = 20
	plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
	plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
	plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
	plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
	plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
	plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize 
	ax = fig.add_subplot(111,aspect='equal')

	for i in range(len(avoid_list)):
		(flag, big_rec) = avoid_list[i]
		rec_2d = big_rec[0:2]
		if rec_2d[0][0] == None and rec_2d[1] == (None,None):
			x_lowerbound = rec_2d[0][1]
		elif rec_2d[0][1] == None and rec_2d[1] == (None,None):
			x_upperbound = rec_2d[0][0]
		elif rec_2d[1][0] == None and rec_2d[0] == (None,None):
			y_lowerbound = rec_2d[1][1]
		elif rec_2d[1][1] == None and rec_2d[0] == (None,None):
			y_upperbound = rec_2d[1][0]
		else:
			x_range = rec_2d[0]
			y_range = rec_2d[1]
			corner, width, height = get_plotter_things(x_range, y_range)
			ax.add_patch(patches.Rectangle(corner, width, height, alpha = 0.5, facecolor = "black",edgecolor = "black"))

	ax.set_xlim([x_lowerbound,x_upperbound])
	ax.set_ylim([y_lowerbound,y_upperbound])

	(flag, Rectangle) = target 
	corner = (Rectangle[0][0],Rectangle[1][0])
	width = Rectangle[0][1] - Rectangle[0][0]
	height = Rectangle[1][1] - Rectangle[1][0]
	ax.add_patch(
		patches.Rectangle(
			corner,   # (x,y)
			width,          # width
			height,          # height
			facecolor="green",
			alpha = 0.5
			)
	)
	for (trajectory, radius_list, _) in trajectory_radius_controller_list:
		ax.scatter([pt[0] for pt in trajectory ],[pt[1] for pt in trajectory ])
		ax.plot([pt[0] for pt in trajectory ],[pt[1] for pt in trajectory ])
		for i in range(len(trajectory)):
			ax.add_patch(
				patches.Rectangle(
					(trajectory[i][0]-radius_list[i][0], trajectory[i][1]-radius_list[i][1]),   # (x,y)
					2 * radius_list[i][0],          # width
					2 * radius_list[i][1],          # height
					fill=False
					)
		)
	# fig.show()
	fig.savefig('figure-2.png')

def main():
	(initial_size, _, A, B, u_space, target, avoid_list, num_steps,u_dim, avoid_dynamic, Theta, safe_rec) = get_benchmark(3)
	(trajectory_radius_controller_list, covered_list, _) = get_controller_yices(Theta, initial_size, A, B, u_dim, u_space, target, avoid_list, avoid_dynamic, safe_rec, num_steps, 1)
	plotter_room(trajectory_radius_controller_list, avoid_list, target, covered_list, Theta)
	
if __name__ == "__main__":
	main()