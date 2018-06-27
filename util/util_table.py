fields = ['#', 'model', 'n', 'm', 'z3-iter', 'z3-time', 'cvc4-iter', 'cvc4-time', 'yices-iter', 'yices-time']

def flatten(benchmark, table_benchmark):
	def flatten_1_21(benchmark, table_benchmark):
		row = [benchmark] + [table_benchmark[k] if k in table_benchmark.keys() else '-' for k in fields[1:]]
		return ",".join([str(c) for c in row])

	def flatten_22_24(benchmark, table_benchmark):
		row = [benchmark]
		row = row + [table_benchmark[k] if k in table_benchmark.keys() else '-' for k in fields[1:4]]

		z3_iter = table_benchmark['z3-iter'] if 'z3-iter' in table_benchmark.keys() else '-'
		z3_iter_n = table_benchmark['z3-iter-n'] if 'z3-iter-n' in table_benchmark.keys() else '-'
		row = row + [str(z3_iter) + " (" + str(z3_iter_n) + ")"]

		z3_time = table_benchmark['z3-time'] if 'z3-time' in table_benchmark.keys() else '-'
		z3_time_n = table_benchmark['z3-time-n'] if 'z3-time-n' in table_benchmark.keys() else '-'
		row = row + [str(z3_time) + " (" + str(z3_time_n) + ")"]

		row = row + [table_benchmark[k] if k in table_benchmark.keys() else '-' for k in fields[6:]]

		return ",".join([str(c) for c in row])

	if(benchmark in [22, 23, 24]):
		return flatten_22_24(benchmark, table_benchmark)
	else:
		return flatten_1_21(benchmark, table_benchmark)

def get_csv_table(table):

	table_rows = []
	table_rows.append(','.join(fields))
	for benchmark in table.keys():
		str_row = flatten(benchmark, table[benchmark])
		table_rows.append(str_row)

	return '\n'.join(table_rows)