#!/bin/bash

# Execute : ./batch_proc.sh input_imgs/

clear

mkdir -p nfs004
mkdir -p nfs005
mkdir -p nfs006
mkdir -p metadata

img_handled=0


start=$(date +"%s")
images=( $(ls "$1") )
for i in ${images[@]}; do 
	echo "Considering : ""$i"" , ""$img_handled"
	mpiexec -n 4 python mpi_convert.py "$PWD""/$1/""$i"
	img_handled=$((img_handled+1))
	
	echo "----------------------------"
	echo "Img handled : ""$img_handled"
	count=$((count+1))
	end=$(date +"%s")
	diff=$(($end-$start))
	echo "Time Taken : ""$(($diff / 60)) minutes and $(($diff % 60)) seconds elapsed."
	echo "-----------------------------"
	rsync -a nfs005/ nfs005:/data/shared/sai/final/nfs005 &
	rsync -a metadata nfs005:/data/shared/sai/final/ &
	rsync -a nfs006/ nfs006:/data/shared/sai/final/nfs006 &
	rsync -a metadata nfs006:/data/shared/sai/final/ &
	if [ $img_handled -eq 60 ]; then
		break
	fi
done

cd ..
