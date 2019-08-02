from pyspark.sql import SparkSession, SQLContext, functions
from creds import USERNAME as UNAME
from creds import PASSWORD as PASS
from datetime import datetime, timedelta
import quinn


SCHEMA = "main_v2"
URL = "jdbc:mysql://localhost:3306/" + SCHEMA
TIME_FMT = '{0:%Y-%m-%d %H:%M:%S}'


spark = SparkSession \
    .builder \
    .appName("Database access example") \
    .config('spark.driver.extraClassPath', './mysql-connector-java-8.0.16.jar') \
    .getOrCreate()

sc = spark.sparkContext
sql_context = SQLContext(sc)
sc.setLogLevel("WARN")


def execute_query(sql_query):
  """
  Executes an arbitrary sql statement and returns the dataframe that is loaded into memory
  """
  # TODO: make generic for each type of clause in a query?
  return sql_context.read.format("jdbc").options(
      url=URL,
      user=UNAME,
      password=PASS,
      query=sql_query).load()


def offset_time_string(datetime_object):
  """
  a nasty solution for fixing the date time offset in queries
  :param datetime_object: datetime_object
  :return: string, to be inserted into queries
  """
  return TIME_FMT.format(datetime_object + timedelta(hours=4))


def get_post_site_text(start_date, end_date):
  """
  method name explains itself
  :param start_date: starting datetime, string
  :param end_date: ending datetime, string
  :return: a spark data frame, starts and ends four hours early relative to queried datetime range
  """
  query = "SELECT siteId, body, dateCreated " + \
          "FROM " + SCHEMA + ".post " + \
          "WHERE dateCreated BETWEEN \"" + \
          start_date + "\" AND \"" + end_date + "\""
  return execute_query(query)


def get_first_post_time(condition=""):
  """
  method name explains itself
  :param condition: a WHERE condition to filter results if needed
  :return: a spark data frame, containing the sorted createdDateTime of the first post satisfying the condition
  """
  query = "SELECT dateCreated " + \
          "FROM " + SCHEMA + ".post " + \
          condition + \
          " ORDER BY dateCreated ASC limit 1"  # first row
  return execute_query(query)


def get_last_post_time(condition=""):
  """
  method name explains itself
  :param condition: a WHERE condition to filter results if needed
  :return: a spark data frame, containing the sorted createdDateTime of the last post satisfying the condition
  """
  query = "SELECT dateCreated " + \
          "FROM " + SCHEMA + ".post " + \
          condition + \
          " ORDER BY dateCreated DESC limit 1"  # last row
  return execute_query(query)


def spark_function_clean_string(spark_column):
  """
  preprocess a string column
  :param spark_column: spark column
  :return: spark function
  """
  # remove non alphabets/whitespaces
  f = functions.regexp_replace(spark_column, "[^\\w\\s]+", "")
  # remove multiple whitespaces
  f = functions.trim(functions.regexp_replace(f, "[ \n]+", " "))
  # all lower case
  f = functions.lower(f)
  return f

def sum_word_counts(df):
  """
  method names explains itself
  case insensitive (all post body converted to lower case)
  :param df: a spark data frame, should contain attribute "body" for post bodies
  :return: a spark data frame containing rows of (word:string, count:int)
  """
  return df.withColumn('word', functions.explode(functions.split(
      spark_function_clean_string(functions.column('body')), ' ')))\
      .groupBy('siteId', 'word')\
      .count()\
      .sort('count', ascending=False) # no need for sorting the results here

def reduce_word_counts(df_1, df_2):
  """
  given two data frames containing word counts of sites from two periods,
  combine them, sum up the common word counts with regard to each site,
  and return the combined counts in a new dat aframe
  :param df_1: first data frame
  :param df_2: second data frame
  :return: new combined data frame
  """
  unioned = df_1.union(df_2)
  return unioned.groupBy('siteId', 'word').agg(functions.sum('count')).withColumnRenamed('sum(count)','count')\
      .sort('count', ascending=False) # no need for sorting the results here


def main():
  start_date = datetime.strptime("2018-03-15", "%Y-%m-%d")
  end_date = datetime.strptime("2018-03-16", "%Y-%m-%d")
  counts_1 = sum_word_counts(get_post_site_text(offset_time_string(start_date), offset_time_string(end_date)))
  counts_2 = sum_word_counts(get_post_site_text(offset_time_string(start_date + timedelta(days=1)), offset_time_string(end_date + timedelta(days=1))))
  counts = reduce_word_counts(counts_1, counts_2)
  counts.show(truncate=False)
  #get_first_post_time().show()


main()
