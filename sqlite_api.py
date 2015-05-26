import os
import time
import sys
import sqlite3
import glob

__author__ = 'saisa_000'

"""
Example: 

py sqlite.py ../adios/TCGA-AA-3870-01Z-00-DX1.txt output/ log/
py sqlite.py ../adios/TCGA-AA-3870-01Z-00-DX1.txt output/

"""

def test_import():
	print "Hello world"
	return

def import_data(input_file, output_file, log_path):

	file_content = open(input_file, 'r')
	
	min_X = 999999
	min_Y = 999999
	max_X = -1
	max_Y = -1
	record_count = 0

	# Create database
	if os.path.exists(output_file):
		os.remove(output_file)
	conn = sqlite3.connect(output_file)

	#  Create table
	header = file_content.readline()
	header = header.strip()
	splitter = header.split('\t')
	create_query = "CREATE TABLE data("
	for column in splitter:
		if column[:10] == "Boundaries":
			column = "Boundaries"
		# print column[:10]
		create_query = create_query + column + ' text' + ', '
	create_query = create_query[:-2] + ")"
	# print create_query
	conn.execute(create_query)
	conn.execute("CREATE INDEX i_xcor ON data (X)") 
	conn.execute("CREATE INDEX i_ycor ON data (Y)") 
	conn.execute("CREATE INDEX i_area ON data (Area)") 
	# Insert data into table
	data_line = file_content.readline()
	while data_line:
		insert_query = "INSERT INTO data VALUES("
		# print "Read : ", data_line
		data_line = data_line.strip()
		splitter = data_line.split('\t')
		min_X = min(min_X, float(splitter[1]) )
		min_Y = min(min_Y, float(splitter[2]) )
		max_X = max(max_X, float(splitter[1]) )
		max_Y = max(max_X, float(splitter[2]) )
		record_count += 1
		for item in splitter:
			insert_query = insert_query + "\'" + item + "\', "
		insert_query = insert_query[:-2] + ")"
		# print insert_query
		conn.execute(insert_query)
		data_line = file_content.readline()
	conn.commit()
	conn.close()
	file_content.close()
	
	'''
	if not os.path.exists(log_path):
		log_content = open(log_path, 'w')
		log_content.write('tile\tmin_X\tmin_Y\tmax_X\tmax_Y\n')
	else:
	'''
	log_content = open(log_path, 'a+')
	log_content.write(output_file + '\t' + str(record_count) + '\t' + str(min_X) + '\t' + str(min_Y) + '\t' + str(max_X) + '\t' + str(max_Y)  + '\n')	
	log_content.close()
	
	return (min_X, min_Y, max_X, max_Y)


def query_x_y_area(min_x, min_y, max_x, max_y, area, db_file, output_file):
	# Sample Queries
	if not os.path.exists(db_file):
		print "No such db file found"
		return
	output = open(output_file, 'a+')
	conn = sqlite3.connect(db_file)
	conn.text_factory = str
	start_time = time.time()
	# print type(min_x), type(min_y), type(max_x), type(max_y), type(area)
	select_query = 	"SELECT * FROM data" \
					+ " WHERE CAST(Area as decimal) > " + str(area) \
					+ " AND CAST(X as decimal) > " + str(min_x) \
					+ " AND CAST(Y as decimal) > " + str(min_y) \
					+ " AND CAST(X as decimal) < " + str(max_x) \
					+ " AND CAST(Y as decimal) < " + str(max_y)
	answers = conn.execute(select_query)
	count = 0
	for answer in answers:
		output.write(str(answer) + '\n')
		count += 1
	end_time = time.time()
	query_time = end_time - start_time
	conn.close()
	output.close()
	return


if __name__ == "__main__":

	"""

	if len(sys.argv) < 3:
		print "Format : "
		print "python file_name input_path output_path log_path"
	else:
		start_time = time.time()
		
		input_path = str(sys.argv[1])
		output_path = str(sys.argv[2]) + '/' + input_path[input_path.rfind('/')+1:-3] + 'db'
		log_path = str(sys.argv[3]) + '/' + 'log_sql.txt'
		
		(min_X, min_Y, max_X, max_Y) = import_data(input_path, output_path, log_path)
		
		end_time = time.time()
		creation_time = end_time - start_time
		# print "Stats : ", (min_X, min_Y, max_X, max_Y)
		print "SQLite Creation Time : ", creation_time
	"""
