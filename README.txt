#####################
EASY WAY
#####################

We have a pre-setup webpage for you to access if you would like here:
http://pdeng.student.rit.edu

If you do want to go through the setup process please continue below, otherwise enjoy!

#####################
Database
#####################

Database Proxy
1. Download the proxy from step 2 here: https://cloud.google.com/sql/docs/mysql/connect-admin-proxy
2. ./cloud_sql_proxy -instances=<INSTANCE_CONNECTION_NAME>=tcp:3306 -credential_file=<PATH_TO_KEY_FILE>

Credentials
Add username and password to the creds.py file in the form

USERNAME = <USERNAME>
PASSWORD = <PASSWORD>

Contact xxd9704@rit.edu for credentials if needed.

######################
Spark
######################
Download spark: https://spark.apache.org/

Download hadoop: https://github.com/steveloughran/winutils/tree/master/hadoop-2.7.1 (this is the windows version). https://hadoop.apache.org/docs/r2.5.2/hadoop-project-dist/hadoop-common/SingleCluster.html (I believe you can find the linux version here)

Download Scala: https://www.scala-lang.org/download/

Download a driver for MYSQL: https://dev.mysql.com/downloads/connector/j/

Install jupyter notebook packages for python if you don't already have them setup.

There is also a dependency on JDK 8 (spark appears to use a jdbc on the backend)

Here are the environment variables that are necessary on windows (they might differ slightly for linux, but are likely very similar)

HADOOP_HOME - the path to the hadoop binaries

JAVA_HOME  - path to jdk 8

SCALA_HOME - path to scala installation

SPARK_HOME - path to spark installation

PYSPARK_PYTHON - the path to your python executable

PYSPARK_DRIVER_PYTHON - the path to the location of the jupyter installation

PYSPARK_DRIVER_PYTHON_OPTS = notebook (this will let  pyspark launch in jupyter notebook)

you  can test if this all worked by typing spark-shell or pyspark (which will launch the notebook)

if you wan't to test a connection to our database, make sure to launch with the arguments:

--driver-class-path <PATH TO MYSQL CONNECTOR JAR>

--jars <PATH TO MYSQL CONNECTOR JAR>

#####################
BOKEH
#####################

Testing
To test an app over an unsecured connection, execute `bokeh serve <filename> --port <portnum>`.

Deployment
To securely deploy an app,
configure an nginx reverse proxy with SSL (https://bokeh.pydata.org/en/latest/docs/user_guide/server.html#reverse-proxying-with-nginx-and-ssl).

Then execute
`bokeh serve <filename> --use-xheaders --allow-websocket-origin=<domain> --port <portnum>`.

Example:
`bokeh serve test_app.py --use-xheaders --allow-websocket-origin=pdeng.student.rit.edu --port 5006`

Dependencies
pip3 install mysql-connector-python
pip3 install bokeh
pip3 install pandas
pip3 install joblib

###############
EXAMPLE DATA
###############

Example data can be found in worldbuilding.meta.stackexcahnge.

###############
NOTES
###############

You can adjust the visualizations by clicking on the wheel zone on the right
then placing the mouse and scrolling on the x axis and y axis to adjust x range and y range, respectively