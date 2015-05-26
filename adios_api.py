#!/usr/bin/env python
"""
Example:

$ python ./test_adios.py
"""
import adios as ad
import numpy as np
import sys
import os
	
def import_data(input_file, output_file, log_path):

	## Writing
	file_content = open(input_file, 'r')

	config = "config_features.xml"
	if len(sys.argv) > 1:
		config = sys.argv[1]

	ad.init("config_features.xml")

	fd = ad.open("feature_list", output_file, "w")

	rows = []
	row = []
	caseid_length = 0
	boundary_length = 0

	header_line = file_content.readline()
	data_line = file_content.readline()
	while data_line:
		data_line = data_line.strip()
		splitter = data_line.split('\t')
		for item in splitter:
			row.append(item)
		rows.append(row)
		row = []
		data_line = file_content.readline()

	data_matrix = np.array(rows)
	data_matrix = np.transpose(data_matrix)

	row_count = data_matrix[0].size
	feature_count = data_matrix.size/data_matrix[0].size
	caseid_length = len(max(data_matrix[0], key=len))
	boundary_length = len(max(data_matrix[-1], key=len))
	groupsize = 4 + 4 + 4 + feature_count*row_count*4 + feature_count*row_count*caseid_length + feature_count*row_count*boundary_length
	# print "Group size : ", groupsize
	ad.set_group_size(fd, groupsize)
	ad.write_int(fd, "row_count", row_count)
	ad.write_int(fd, "case_length", caseid_length)
	ad.write_int(fd, "boundary_length", boundary_length)

	# Writing records into bp file
	i = 0
	splitter = header_line.split('\t')
	for feature in splitter:
		# print feature, ' : ', len(data_matrix[i])
		if feature == "Slide":
			ad.write(fd, feature, data_matrix[i].tolist())
		elif feature[:10] == "Boundaries":
			ad.write(fd, "Boundaries", data_matrix[i].tolist())
		else:
			ad.write(fd, feature, data_matrix[i].astype(np.float))
		i += 1

	ad.close(fd)

	ad.finalize()
	
	log_content = open(log_path, 'a+')
	log_content.write(output_file + '\t' + str(len(data_matrix[0])) + '\t' + str(np.min(data_matrix[1].astype(np.float))) + '\t' + str(np.min(data_matrix[2].astype(np.float))) + '\t' + str(np.max(data_matrix[2].astype(np.float))) + '\t' + str(np.max(data_matrix[2].astype(np.float)))  + '\n')	
	log_content.close()
	
def query_x_y_area(min_x, min_y, max_x, max_y, area, input_file, output_file):

	## Querying
	min_x = int(min_x)
	min_y = int(min_y)
	max_x = int(max_x)
	max_y = int(max_y)
	area = int(area)

	f = ad.file(input_file)
	# print f.var.keys()
	
	# print " ---Area--- "
	v = f.var['Area']
	val = v.read()
	area_bound = np.where( val > area )
	
	# print " ---X--- "
	v = f.var['X']
	val = v.read()
	minx_bound = np.where( val > min_x )
	bound = np.intersect1d(area_bound[0], minx_bound[0])
	
	maxx_bound = np.where( val < max_x )
	bound = np.intersect1d(bound, maxx_bound[0])
	
	# print " ---Y--- "
	v = f.var['Y']
	val = v.read()
	miny_bound = np.where( val > min_y )
	bound = np.intersect1d(bound, miny_bound[0])
	
	maxy_bound = np.where( val < max_y )
	bound = np.intersect1d(bound, maxy_bound[0])
	
	# print 'Bound : ', bound
	print 'Items found in ', input_file, ' : ', len(bound)
	if len(bound) < 2:
		f.close()
		return
	
	output_data = []
	for keys in f.var.keys():
		# output_line = []
		if "Boundaries" in str(keys) or "Slide" in str(keys):
			v = f.var[keys]
			val = v.read()
			val= val[bound] # Bounding data as per query
			temp = []
			for item in val:
				temp_item = np.trim_zeros(item)
				string =  str(temp_item.tostring())
				# output_write.write(string + '\t')
				temp.append(string)
			output_data.append(temp)
		elif "row_count" not in str(keys) and "boundary_length" not in str(keys) and "case_length" not in str(keys):
			v = f.var[keys]
			val = v.read()
			if len(val) == 0:
				print 'Value for ', keys, ' : ', val
			val= val[bound] # Bounding data as per query
			output_data.append(val)
	output_data = np.array(output_data)
	output_data = np.transpose(output_data)
	
	headers = []
	output_write = file(output_file, 'a')
	np.savetxt(output_write, output_data, delimiter='\t',fmt="%s")
	output_write.close()
	f.close()

if __name__ == '__main__':
	input_file = str(sys.argv[1])
	import_data(input_file, 'test_adios.bp', 'log_test_adios.text')
