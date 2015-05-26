#!/usr/bin/env python
"""
Example:

$ mpiexec -n 4 python ./mpi_convert.py results.txt
"""

from mpi4py import MPI
import sys
import os
import itertools
import sqlite_api
import adios_api
import subprocess

size = MPI.COMM_WORLD.Get_size()
rank = MPI.COMM_WORLD.Get_rank()
name = MPI.Get_processor_name()

output = ['nfs004', 'nfs005', 'nfs006']
turn = 0
files_handled = 0

FNULL = open(os.devnull, 'w')

if __name__ == "__main__":

	input_file = str(sys.argv[1])
	if rank == 0:
		print 'Processing image : ', input_file
	file_content = open(input_file, 'r')
	nthline = itertools.islice(file_content, rank, None, size)
	
	# print sum(1 for _ in nthline)
	for line in nthline:
		line = line.rstrip()
		
		# convert 'line' to sqlite
		output_path = output[turn] + '/' + line[line.rfind('/')+1:-3] + 'db'
		sqlite_api.import_data(line, output_path, 'metadata/log_sql.txt')
		
		# convert 'line' to ADIOS
		output_path = output[turn] + '/' + line[line.rfind('/')+1:-3] + 'bp'
		adios_api.import_data(line, output_path, 'metadata/log_adios.txt')
		
		# convert 'line' to hdt
		output_path = output[turn] + '/' + line[line.rfind('/')+1:-3] + 'hdt'
		subprocess.call(['java', 'hdt_convert', line, output[turn], 'metadata'], stdout=FNULL, stderr=subprocess.STDOUT)
		
		turn = (turn+1) % 3
		files_handled += 1
