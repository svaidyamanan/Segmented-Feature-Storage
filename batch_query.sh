#!/bin/bash

# Execute : ./batch_query.sh metadata/log_sql.txt results.txt

start=$(date +"%s")

pids=""

mpiexec -n 8 python ./mpi_query_nfs004.py $1 $2 &
pids="$pids $!"
ssh nfs005 /data/shared/sai/final/batch_query_remote.sh $1 $2 &
pids="$pids $!"
ssh nfs006 /data/shared/sai/final/batch_query_remote.sh $1 $2 &
pids="$pids $!"
wait $pids

mkdir -p output
cp $2 "output/""${2:0:${#2}-4}""_004.txt"

end=$(date +"%s")
diff=$(($end-$start))
echo "Time Taken : ""$(($diff / 60)) minutes and $(($diff % 60)) seconds elapsed."
