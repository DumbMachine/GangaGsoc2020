The below section deals with graphs and possible explanations of results obtained after bench marking 5 different databases. The code used to benchmark databases, can be found here. 

# Plots for Database Comparison:

1. Comparison of `MongoDB` and `PostgreSQL` for storing a ganga job metadata:

   ![image](src/bench/draw/mongo_time.png)![image](src/bench/draw/postgres_time.png)![image](src/bench/draw/total_time.png)

2. Comparison of the Resources used by `MongoDB` and `Postgres` docker instance:

   NOTE: The reference sections for `postgres` graphs are longer as it took more time to perform the same tasks)

   The information was captured using this scripts that can be found [here](https://github.com/DumbMachine/GangaGsoc2020/tree/master/src/bench) :

   ![src/bench/images/cpu_usage_percent.png](src/bench/images/BLOCK.png)![image](src/bench/images/NETIO.png)![image](src/bench/images/cpu_usage_percent.png)![image](src/bench/images/mem_usage_percent.png)![image](src/bench/images/MEM_USAGE.png)

   

# Plots for Job Conversion Methods Comparison:

NOTE: `full_print` method by itself isn't viable but is included as it was asked fore in the early edit of Qualification Task for this project.

![image](src/task2/2.3/data/mongo-method-full_print-1000-time_interval-0.png)![image](src/task2/2.3/data/mongo-method-export-1000-time_interval-0.png)![image](src/task2/2.3/data/mongo-method-xml -1000-time_interval-0.png)

