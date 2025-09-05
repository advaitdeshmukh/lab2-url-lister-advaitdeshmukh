## Steps to replicate results(CSEL):

1. make prepare -> this will download the input files
2. hdfs dfs -rm -r -f output-stream || true -> Delete any paths from last run
3. mapred streaming \
   -files URLMapper.py,URLReducer.py \
   -mapper "python3 URLMapper.py" \
   -reducer "python3 URLReducer.py"\
   -input input\
   -output output-stream -> Run streaming MapReduce to get URLCounts
4. hdfs dfs -cat output-stream/part-00000 | LC_ALL=C sort -> View URLCounts (Also available in results_csel.txt)

## Steps to run on gcloud:
4 workers example:
1. gcloud dataproc clusters create urlcount-4w \
  --region=us-central1 \
  --zone=us-central1-a \
  --num-workers=4 \
  --image-version=2.3-debian12 \
  --master-boot-disk-size=100 \
  --worker-boot-disk-size=100 -> Spin up a cluster
2. gcloud compute ssh urlcount-4w-m --zone=us-central1-a -> ssh into Master node
3. git clone https://github.com/advaitdeshmukh/lab2-url-lister-advaitdeshmukh.git || true -> Clone repo
4. cd lab2-url-lister-advaitdeshmukh
5. make prepare -> Download required files
6. hdfs dfs -rm -r -f output-stream || true -> Delete any old output-stream
7. { time -p mapred streaming \
  -files URLMapper.py,URLReducer.py \
  -mapper "python3 URLMapper.py" \
  -reducer "python3 URLReducer.py" \
  -input input \
  -output output-stream ; } 2> timing_4w.txt -> Run the job + time it
8. hdfs dfs -ls output-stream
9. hdfs dfs -getmerge output-stream results_dataproc_4w.txt -> Merge output files
10. LC_ALL=C sort -o results_dataproc_4w.txt results_dataproc_4w.txt -> Sort the results for easy comparison

   
