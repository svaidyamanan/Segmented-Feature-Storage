#!/bin/bash

mkdir -p /data/shared/sai/code/input_imgs
my_array=( $(find /data/shared/tcga_analysis/ -maxdepth 1 -type d -name '*svs') )

for i in ${my_array[@]}; do 
	
	cd "$i""/output"
	
	path="${i##*/}";
	path="${path%???}""txt"
	ls -d -1 $PWD/*.* > "/data/shared/sai/code/input_imgs/""$path"
	
	cd ../..
done
