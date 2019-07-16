#####################
Database
#####################

Database Proxy
1. Download proxy from x link <- we could just include this in our source to make it easy for him
2. run start.bat to start proxy

Creds
Add username and password to the creds.py file

Need to give credentials file as well somehow
and the server name


######################
Spark
######################
Download spark: https://spark.apache.org/

Download hadoop: https://github.com/steveloughran/winutils/tree/master/hadoop-2.7.1 (this is the windows version). https://hadoop.apache.org/docs/r2.5.2/hadoop-project-dist/hadoop-common/SingleCluster.html (I believe you can find the linux version here)

Download Scala: https://www.scala-lang.org/download/

Download a driver for MYSQL: https://dev.mysql.com/downloads/connector/j/

Install jupyter notebook packages for python if you don't already have them setup.

There is also a dependency on JDK 8 (spark appears to use a jdbc on the backend)

Here are the environent variables that are necessary on windows (they might differ slightly for linux, but are likely very similar)

HADOOP_HOME - the path  to the  hadoop binaries

JAVA_HOME  - path  to jdk 8

SCALA_HOME - path to scala installation

SPARK_HOME - path to spark installation

PYSPARK_PYTHON - the path to your python executable PYSPARK_DRIVER_PYTHON - the path to the location of the jupyter installation PYSPARK_DRIVER_PYTHON_OPTS = notebook (this will let  pyspark launch in jupyter notebook)

you  can test if this all  worked by typing spark-shell or pyspark (which will launch the notebook)

if you wan't to test a connection to our database, make sure to launch with the arguments --driver-class-path <PATH TO MYSQL CONNECTOR JAR> --jars <PATH TO MYSQL CONNECTOR JAR>

