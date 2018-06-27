from optparse import OptionParser

solvers = ['z3', 'yices', 'cvc4']

def get_cmd_opts():
    parser = OptionParser()
    parser.add_option("-s", "--solver", action="store", dest="solver", choices=solvers, help="SMT solver. One of 'z3', 'yices' or 'cvc4' [OPTIONAL]. Default : 'z3' ")
    parser.add_option("-b", "--benchmark", action="store", type="string", dest="benchmark", help="Benchmark from the main paper (integer in [1,24]) [REQUIRED]")
    parser.add_option("-p", "--print-controller", action="store_true", dest="printcontroller", help="Print controller description.")
    parser.add_option("-n", "--non-incremental", action="store_true", dest="nonincremental", help="Use z3's non-incremental solver for benchmark(s) 22, 23 or 24 from the main paper [OPTIONAL].")

    (options, args) = parser.parse_args()
    solver = 'z3'
    if not(options.solver is None):
        if (options.solver in solvers):
            solver = options.solver
        else:
            parser.error("Illegal solver option")    

    benchmark = None
    if options.benchmark is None:
        parser.error("Benchmark not provided !")
    elif not options.benchmark.strip():
        parser.error("Benchmark is invalid !")
    elif not options.benchmark.isdigit():
        parser.error("Benchmark is invalid !")
    else:
        benchmark = int(options.benchmark)
        if ((benchmark < 1) or (benchmark > 24)):
            parser.error("Benchmark should be an integer in [1, 24] !")

    printcontroller = False
    if not (options.printcontroller == None):
        printcontroller = options.printcontroller

    nonincremental = False
    if not (options.nonincremental == None):
        if (benchmark in [22, 23, 24] and solver == 'z3'):
            nonincremental = options.nonincremental
        else:
            parser.error("The non-incremental option should be used only for benchmarks 22, 23 or 24 and when the solver is z3 !")

    if not (len(args) == 0):
        parser.error('Unnecessary argument(s) : ' + ' '.join(args))

    return (solver, benchmark, printcontroller, nonincremental)

def get_cmd_opts_runall():
    parser = OptionParser()
    parser.add_option("-s", "--solver", action="store", dest="solver", choices=solvers + ["all"], help="SMT solver. One of 'z3', 'yices', 'cvc4' or 'all' [OPTIONAL]. Default : 'all' ")
    parser.add_option("-c", "--compile", action="store_true", dest="table", help="Compile results into a a CSV table.")
    parser.add_option("-t", "--timeout-examples", action="store_true", dest="timeout", help="Run all benchmark-solver combinations (including those that take a lot of time).")

    (options, args) = parser.parse_args()
    solver = 'all'
    if not(options.solver is None):
        if (options.solver in solvers + ['all']):
            solver = options.solver
        else:
            parser.error("Illegal solver option")
    if not (len(args) == 0):
        parser.error('Unnecessary argument(s) : ' + ' '.join(args))

    table = False
    if not (options.table == None):
        table = options.table

    timeout = False
    if not (options.timeout == None):
        timeout = options.timeout

    return (solver, table, timeout)
