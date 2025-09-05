# Lab 2: UrlCount (Python Streaming)

## Overview:
 I did this exercise using Hadoop Streaming in Python. The mapper extracts all the text that looks like a link (using regex) and emits a <url, 1> for each of the instance. The reducer sums counts per URL and prints the totals only if they are more than 5.

## Software/Environment required:
1. CSEL: Hadoop 3.x, Python 3.x
2. Google Cloud Dataproc Specifics:
     - region: us-central1
     - zone: us-central1-a
     - image: 2.3-debian12

## Dataproc results comparison (2 workers vs 4 workers):
A (slightly) surprising result I found was that 4 worker setup took marginally longer than 2 worker setup (73.48s for 2 workers opposed to 74.86s for 4 workers). I believe this can happen because of the large overheads compared to the actual task. As we scale the amount of data being processed I expect 4 worker setup to be faster than 2 worker setup.

## Outputs:
Here's the URLs that appear more than 5 times with their respective counts:
```
#	20
/wiki/Doi_(identifier)	18
/wiki/Google_File_System	6
/wiki/ISBN_(identifier)	18
/wiki/MapReduce	7
/wiki/S2CID_(identifier)	14
mw-data:TemplateStyles:r1129693374	7
mw-data:TemplateStyles:r1238218222	121
mw-data:TemplateStyles:r1295599781	33
mw-data:TemplateStyles:r886049734	12
```

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

## Resources & collaboration
- Piazza posts that brought up common issues + Professor's post about updated requirement
- Collaboration: worked independently + used chatGPTs assistance for debugging GCloud cluster creation issues
