from pyspark.sql import SparkSession, SQLContext, functions
from creds import USERNAME as UNAME
from creds import PASSWORD as PASS

URL = "jdbc:mysql://localhost:3306/main2"

spark = SparkSession \
    .builder \
    .appName("Database access example") \
    .config('spark.driver.extraClassPath', './mysql-connector-java-8.0.16.jar') \
    .getOrCreate()

sc = spark.sparkContext
sql_context = SQLContext(sc)
sc.setLogLevel("INFO")


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


def get_post_site_text(start_date, end_date):
  """
  method name explains itself
  :param start_date: starting datetime, string
  :param end_date: ending datetime, string
  :return: a spark data frame, starts and ends four hours early relative to queried datetime range
  """
  query = "SELECT site.siteId, post.body, post.createdDateTime " + \
          "FROM main2.site INNER JOIN main2.post ON site.siteId = post.siteId " + \
          "WHERE createdDateTime BETWEEN \"" + \
          start_date + "\" AND \"" + end_date + "\"" #+ \
          #" ORDER BY createdDateTime DESC limit 1"  # last row
          #" ORDER BY createdDateTime ASC limit 1"  # first row
  # string formatting could make more readable
  return execute_query(query)


def sum_word_count(df):
  """
  method names explains itself
  :param df: a spark data frame, should contain attribute "body" for post bodies
  :return: a spark data frame containing rows of (word:string, count:int)
  """
  return df.withColumn('word', functions.explode(functions.split(functions.column('body'), ' ')))\
      .groupBy('siteId', 'word')\
      .count()#\
      #.sort('count', ascending=False) # no need for sorting the results here


def main():
  posts = get_post_site_text("2018-03-15", "2018-03-16")
  counts = sum_word_count(posts)
  counts.show(500)
  # execute_query("SELECT siteId FROM main2.site").show(500)


main()
