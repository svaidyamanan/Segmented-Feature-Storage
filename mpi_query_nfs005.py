#!/usr/bin/env python
"""
Example:

$ mpiexec -n 4 python ./mpi_query.py log_sql.txt results.txt
"""

from mpi4py import MPI
import sys
import os
import itertools
import sqlite_api
import subprocess
import adios_api

size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()

files_handled = 0

FNULL = open(os.devnull, 'w')

if __name__ == "__main__":

	input_file = str(sys.argv[1])
	output_file = str(sys.argv[2])
	
	nthline = []
	file_content = open(input_file, 'r')
	data_line = file_content.readline()
	while data_line:
		if 'nfs005' in data_line:
			nthline.append(data_line)
		data_line = file_content.readline()
	
	nthline = nthline[rank::size]
	# nthline = itertools.islice(file_content, rank, None, size)
	
	# print sum(1 for _ in nthline)
	for line in nthline:
		line = line.rstrip()
		line = line.split()[0]
		# print 'Searching in : ', line
		# Query sqlite file
		# sqlite_api.query_x_y_area(-1, -1, 999999, 999999, 200, line, output_file)
		adios_api.query_x_y_area(-1, -1, 999999, 999999, 0, line, output_file)
		# subprocess.call(['java', 'hdt_query', line, '200', output_file]) #, stdout=FNULL, stderr=subprocess.STDOUT)
		files_handled += 1
