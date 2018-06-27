# RealSyn : Tool Companion for "Controller Synthesis Made Real", Fan et. al., CAV2018

## Introduction

RealSyn synthesizes controllers for discrete-time linear dynamical systems 
against reach-avoid specifications.
The details of the technical aspect of the approach are outlined in our paper
**Controller Synthesis Made Real: Reach-avoid Specifications and Linear Dynamics**.
The tool is implemented in Python.

## VM image
Users not wanting to install the pre-requisite libraries can download a virtual machine.
The instructions for obtaining RealSyn VM can be downloaded from : [https://uofi.app.box.com/v/realsynInstructions](https://uofi.app.box.com/v/realsynInstructions) .

## Installation (Skip if you are using the VM)

**The provided VM comes with pre-installed libraries. You can skip this section if you are using the VM provided for CAV'18 Artifact Evaluation.**

RealSyn relies on the Python bindings of the following libraries:

	1. CVXOPT
	2. PICOS
	3. numpy scipy matplotlib
	4. slycot (this may require fortran compiler which comes from gcc)
	5. control
	6. SMT solvers: z3, Yices2, CVC4

As long as at least one of the SMT solvers is present, RealSyn can be run successfully.
If only a subset of the proposed solvers are available, comment the appropriate imports from 

## Disclaimer : 
** The VM (.ova file) has only been tested on `VirtualBox` on Linux and MacOS. 
We are seeing very different results like core dump on other platforms using exactly 
the same .ova file **

## Reproducing the results from the paper

### Table-1

1. First, enter the directory `RealSyn` :
```
cd RealSyn/
```

2. The file `realsyn.py` can be used to run specific benchmarks on specific solvers. 
See its usage below:
```
python realsyn.py -h
```

2.1  To run some benchmark from Table-1 in the paper on some solver, run:
```
python realsyn.py -b <benchmark_number> -s <solver>
```
Here, `<benchmark_number>` can be any integer in [1,24] and <solver> can be one of `z3`, `yices` or `cvc4`.

For example, to run the 15th benchmark, with `CVC4`, run:
```
python realsyn.py -b 15 -s cvc4
```

** Remark ** Some of the benchmarks (especially those with high dimensions)
may not run fast, and it a slow-down of about 5x should be expected.
This is because, the RAM of the VM is set to 4GB and the experiments in 
the paper have been performed on a RAM of 16GB.

2.2 To run non-incremental `z3` on benchmarks `22`, `23` and `24`, run :
```
python realsyn.py -b <benchmark_number> -s z3 -n
```
The option `-n` works only for the benchmarks `22`, `23` and `24` with `z3` solver.

2.3 To print the controller synthesized, add the flag `-p` to the usual command.
For example, in order to print the controller synthesized on benchmark-1 with Yices solver, execute:
```
python realsyn.py -b 1 -s yices -p
```

The output will look like this:
```
 ############## Printing Controller ##############

K (common to all trjaectories) = [[-1.44160279  1.0782186 ]]

Sub-controllers:

********* 0 *********
x_ref[0] = [1.0, 1.0]

controller (control input for each time-step) = 
Step# 0: [-0.78283869980868]
Step# 1: [-0.17488417526027933]
Step# 2: [0.4852857750658994]
Step# 3: [-2.0]
Step# 4: [1.0014825567846675]
Step# 5: [-2.0]
Step# 6: [2.0]
Step# 7: [0.9804339358168611]
Step# 8: [2.0]
Step# 9: [-0.3149935955072204]

Subset of Theta covered by this controller = 
Rectangle: [(0.5757318625371235, 1.4242681374628765), (0.5757318625371235, 1.4242681374628765)]
************************* 

********* 1 *********
x_ref[0] = [1.5, 1.2000548263294182]

controller (control input for each time-step) = 
Step# 0: [-1.5374592847467499]
Step# 1: [0.39915757026487225]
Step# 2: [0.4418438504583897]
Step# 3: [-2.0]
Step# 4: [1.704228080238866]
Step# 5: [-2.0]
Step# 6: [2.0]
Step# 7: [-2.0]
Step# 8: [2.0]
Step# 9: [-0.3300654327649058]

Subset of Theta covered by this controller = 
Rectangle: [(1.0757318625371235, 1.9242681374628765), (0.7757866888665417, 1.6243229637922947)]
************************* 

********* 2 *********
x_ref[0] = [1.441473051523213, 0.7585817748062048]

controller (control input for each time-step) = 
Step# 0: [-0.9024550057853774]
Step# 1: [0.7990334796695446]
Step# 2: [-0.5030831270489239]
Step# 3: [-0.2867023991028679]
Step# 4: [-2.0]
Step# 5: [-2.0]
Step# 6: [2.0]
Step# 7: [1.0960900037944745]
Step# 8: [2.0]
Step# 9: [-0.28324347163082825]

Subset of Theta covered by this controller = 
Rectangle: [(1.0172049140603365, 1.8657411889860895), (0.33431363734332825, 1.1828499122690814)]
************************* 

********* 3 *********
	.
	.
	.
	.
	.
```
Here, the matrix `K` and each of the sub-controllers describe the overall controller
(refer Algorithm-1 in the main paper).
Each subcontroller drives a portion of the initial set `Theta` to the 
target set while staying in the safe set.
A subcontroller is described by three components:
- Initial point in the reference trajectory (`x_Ref[0]`)
- Control signal
- Subset of Theta for which this control signal drives the system while meeting the reach-avoid specification.


3. The file `runall.py` can be used to run all our examples. To see usage, run :
```
python runall.py -h
```

3.1. To run all the benchmarks on each of the solvers, execute the following command (see remark below):
```
python runall.py
```
The above command runs all (benchmark, solver) combinations except for the combinations that time-out in the paper (see our paper for reference):
a) Benchmark-22 on z3 (incremental solver)
b) Benchmark-24 on z3 (incremental solver)
c) Benchmark-3  on z3
d) Benchmark-3  on cvc4
e) Benchmark-23 on cvc4
f) Benchmark-22 on yices

** Remark ** Because some of the examples can take a very long time (more than 1 hour),
especially on the supplied VM (because of limited RAM available), 
it is advisable to run these examples overnight. The expected running time is more than 5 hours.
Better still, run the script `runall_fast.py` (described in point 4.).
That is, if you are crunched for time and want to quickly check if this
tool "works", skip all the below items and go directly to point-4.

3.2. In order to include the above (time-out) benchmarks also, run:
```
python runall.py -t
```

3.3 If you want to compile the table in a CSV format, add the `-c` flag to the appropriate command.
So for example, if you want to compile the table for all benchmark-solver combinations (including those that might time out), you should run:
```
python runall.py -t -c
```
To generate the table without the expensive benchmarks, run:
```
python runall.py -c
```

3.4. To run the benchmarks on a specific solver, add the `-s <solver>` option:
```
python runall.py -s <solver>
```
Here, `<solver>` can be one of `z3` (for z3 solver), `cvc4` (for CVC4 solver), `yices` (for Yices solver) or `all` (for all solvers---so basically the option `-s all` serves the same purpose as not supplying this flag at all).

As before, the additional options `-t` and `-c` can also be supplied with the `-s <solver>` option.

4. The file `runall_fast.py` can be used to run all the **fast** benchmarks (in the range [11,21]). 
To see usage, run :
```
python runall_fast.py -h
```

4.1. To run all the **fast** benchmarks on each of the solvers, execute the following command:
```
python runall_fast.py
```

4.2 If you want to compile the results in a CSV format, add the `-c` flag 
to the appropriate command.
So for example, if you want to compile the table for all (**fast** benchmark, solver) 
combinations, you should run:
```
python runall_fast.py -c
```

4.3. To run the **fast** benchmarks on a specific solver, add the `-s <solver>` option:
```
python runall_fast.py -s <solver>
```
Here, `<solver>` can be one of `z3` (for z3 solver), `cvc4` (for CVC4 solver), `yices` (for Yices solver) or `all` (for all solvers---so basically the option `-s all` serves the same purpose as not supplying this flag at all).

As before, the additional option `-c` can also be supplied with the `-s <solver>` option.

### Figure-2

Run the following command:
```
python generate_figure.py
```
This will generate file `figure-2.png` in the source folder `RealSyn`.

** Remark ** : The figure differs from the one presented in the paper
because there we plotted two different trajectories, but here, we are just plotting 
a single trajectory.

## How to run your own benchmark :

Running your benchmark is easy !
All the benchmarks are located in the folder `RealSyn/benchmarks/`.
In what follows, we assume that your in this folder already.

1. First, take a look at any of the existing benchmarks.
For example:
```
gedit benchmarks/example1.py &
```
How to interpret this file?
(a) The function `name()` returns the name of the benchmark. 
The return type of this function is a Python string

(b) The function `problem()` defines the crux of the problem.
It returns the parameters of the linear dynamical system (dynamics, etc),
safety set, avoid sets, etc. Here is a detailed description:
	- `A, B`: dynamic of the system, `x[t+1] = A x[t] + B u[t]`
	- `Theta`: initial set
	- `initial_size, center` : obsolete now. Please ignore.
	- `u_space`: input space
	- `target`: goal set
	- `avoid_list`: static avoid sets, fixed for every time step
	- `avoid_dynamic`: dynamic avoid set, specifies different avoid set at each time step
	- `num_steps`: total time steps for the synthesis
	- `u_dim`: input space dimension
	- `safe_rec`: used only if there is only a safe region that the system should stay in and no avoid sets (avoid is the complement of the safe region)

For sets, we have two representations:
	- `(True, bound_list)` means the set is a rectangle, and `bound_list` specifies the upper and lower bound of each dimension of the rectangle 
	- `(False, (M,v))` means the set is a general polytope represented as `M*x + v <= 0 `

2. That's it! You are now good to go !
In order to add your own benchmark (let's call it `example25` named `foo`):

(a) Copy some existing benchmark file (say `example1.py`) :
```
cp example1.py example25.py
```

(b) Edit the parameters as described above in point-1.

(c) Run the `realsyn.py` script on your example:
```
cd ../ #go to the source directory
python realsyn.py -b 25 -s yices
```
