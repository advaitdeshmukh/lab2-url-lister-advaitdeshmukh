## Steps to replicate results:

1. make prepare -> this will download the input files
2. hdfs dfs -rm -r -f output-stream || true -> Delete any paths from last run
3. mapred streaming        -files URLMapper.py,URLReducer.py       -mapper "python3 URLMapper.py"          -reducer "python3 URLReducer.py"        -input input        -output output-stream -> Run streaming MapReduce to get URLCounts
4. hdfs dfs -cat output-stream/part-00000 | LC_ALL=C sort -> View URLCounts (Also available in results_csel.txt)