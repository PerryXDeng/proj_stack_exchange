from textblob import TextBlob
from pyspark.sql import SparkSession, SQLContext, functions
from creds import USERNAME as UNAME
from creds import PASSWORD as PASS
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, DAILY
from nltk.corpus import stopwords
from concurrent.futures import ThreadPoolExecutor

SCHEMA = "main_v2"
PERFORMANCE_PILL = "?useServerPrepStmts=false&rewriteBatchedStatements=true"
URL = "jdbc:mysql://localhost:3306/" + SCHEMA + PERFORMANCE_PILL
TIME_FMT = '{0:%Y-%m-%d %H:%M:%S}'
JDBC_PROPERTIES = {"user":UNAME, "password":PASS}

def execute_query(sql_context, sql_query):
  """
  Executes an arbitrary sql statement and returns the data frame
  :param sql_context: spark sql context
  :param sql_query: arbitrary query
  """
  return sql_context.read.format("jdbc").options(
      url=URL,
      user=UNAME,
      password=PASS,
      query=sql_query).load()


def insert_df_to_table(df, table_name):
  """
  method name explains itself
  :param df: spark data frame
  :param table_name: sql table name
  :return: None
  """
  df.write.jdbc(
      url=URL,
      table=table_name,
      mode="append",
      properties=JDBC_PROPERTIES)


def offset_time_string(datetime_object):
  """
  a nasty solution for fixing the date time offset in queries
  :param datetime_object: datetime_object
  :return: string, to be inserted into queries
  """
  return TIME_FMT.format(datetime_object + timedelta(hours=4))


def get_post_site_count(sql_context, start_date, end_date):
  """
  method name explains itself, count the number of posts by site
  :param sql_context: spark sql
  :param start_date: starting datetime, string
  :param end_date: ending datetime, string
  :return: a spark_session data frame, starts and ends four hours early relative to queried datetime range
  """
  query = "SELECT siteId, COUNT(*) as posts_count " + \
          "FROM " + SCHEMA + ".post " + \
          "WHERE dateCreated BETWEEN \"" + \
          start_date + "\" AND \"" + end_date + "\" " + \
          "GROUP BY siteId"
  return execute_query(sql_context, query)


def get_first_post_time(sql_context, condition=""):
  """
  method name explains itself
  :param sql_context: spark sql
  :param condition: a WHERE condition to filter results if needed
  :return: a spark_session data frame, containing the sorted createdDateTime of the first post satisfying the condition
  """
  query = "SELECT dateCreated " + \
          "FROM " + SCHEMA + ".post " + \
          condition + \
          " ORDER BY dateCreated ASC limit 1"  # first row
  return execute_query(sql_context, query)


def get_last_post_time(sql_context, condition=""):
  """
  method name explains itself
  :param sql_context: spark sql
  :param condition: a WHERE condition to filter results if needed
  :return: a spark_session data frame, containing the sorted createdDateTime of the last post satisfying the condition
  """
  query = "SELECT dateCreated " + \
          "FROM " + SCHEMA + ".post " + \
          condition + \
          " ORDER BY dateCreated DESC limit 1"  # last row
  return execute_query(sql_context, query)


def spark_function_clean_string(spark_column):
  """
  preprocess a string column
  :param spark_column: spark_session column
  :return: spark_session function
  """
  # remove formatting and html entities
  f = functions.regexp_replace(spark_column, "(<(.*)>)|(&(amp|lt|gt);)", " ")
  # remove non alphabets/whitespaces and replace with whitespace
  f = functions.regexp_replace(f, "[^\\w\\s]+", " ")
  # remove multiple whitespaces
  f = functions.trim(functions.regexp_replace(f, "[ \n\t\r]+", " "))
  # all lower case
  f = functions.lower(f)
  return f


def get_post_site_text(sql_context, start_date, end_date):
  """
  method name explains itself
  :param sql_context: spark sql
  :param start_date: starting datetime, string
  :param end_date: ending datetime, string
  :return: a spark_session data frame, starts and ends four hours early relative to queried datetime range
  """
  query = "SELECT siteId, postId, body " + \
          "FROM " + SCHEMA + ".post " + \
          "WHERE dateCreated BETWEEN \"" + \
          start_date + "\" AND \"" + end_date + "\""
  return execute_query(sql_context, query)


def sum_post_word_counts_by_site(df):
  """
  method names explains itself
  case insensitive (all post body converted to lower case)
  :param df: a spark_session data frame, should contain attribute "body" for post bodies
  :return: a spark_session data frame containing rows of (word:string, count:int)
  """
  processed = df.withColumn('word', functions.explode(functions.split(
      spark_function_clean_string(functions.column('body')), ' ')))
  df.unpersist() # free memory
  truncated = processed.withColumn('word', functions.substring(processed.word, 1, 20))
  processed.unpersist()
  summed = truncated.groupBy('siteId', 'word').count().filter(truncated.word != "")
  truncated.unpersist()
  return summed


def reduce_word_counts(df_1, df_2):
  """
  given two data frames containing word counts of sites from two periods,
  combine them, sum up the common word counts with regard to each site,
  and return the combined counts in a new dat aframe
  :param df_1: first data frame
  :param df_2: second data frame
  :return: new combined data frame
  """
  if df_1 is None:
    # for iteration zero when there is no existing df to merge with
    return df_2
  union = df_1.union(df_2)
  df_1.unpersist()  # free memory
  df_2.unpersist()  # free memory
  reduced = union.groupBy('siteId', 'word').agg(functions.sum('count')).withColumnRenamed('sum(count)','count')
  union.unpersist()
  return reduced


def word_frequencies_for_month(sql_context, date:datetime, stop_words:set):
  month_start = date.replace(day=1)
  month_end = month_start + relativedelta(months=+1)
  df = None
  for day in rrule(DAILY, dtstart=month_start, until=month_end):
    start = offset_time_string(day)
    end = offset_time_string(day + timedelta(days=1))
    df = reduce_word_counts(df, sum_post_word_counts_by_site(get_post_site_text(sql_context, start, end)))
  posts_counts = get_post_site_count(sql_context, offset_time_string(month_start), offset_time_string(month_end))
  joined = df.join(posts_counts, "siteId")
  df.unpersist()
  frequencies = joined.select(functions.column("siteId"), functions.column("word"),
              (functions.column("count")/functions.column("posts_count")).alias("frequency"))
  joined.unpersist()
  # filter out irrelevant words
  filtered = frequencies.filter(frequencies.word.isin(stop_words) == False)
  frequencies.unpersist()
  return filtered


def create_stop_words():
  # ignore common English words
  stop_words = set(stopwords.words('english'))
  # # ignore Python keywords and builtin types
  # stop_words.update({'false', 'none', 'true', 'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del', 'elif',
  #                    'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
  #                    'nonlocal', 'not', 'or', 'pass', 'raise', 'try', 'while', 'with', 'yield',
  #                    'int', 'float', 'complex', 'bool', 'abs', 'divmod', 'pow', 'round', 'str', 'xrange', 'set',
  #                    'frozenset', 'dict', 'len', 'iter', 'open', 'memoryview', 'range', 'enumerate', 'bytearray'})
  # # ignore VBA keywords
  # stop_words.update({'alias', 'as', 'base', 'boolean', 'byte', 'byref', 'byval', 'call', 'case', 'cbool', 'cbyte',
  #                    'ccur', 'cdate', 'cdbl', 'cint', 'clng', 'clnglng', 'compare', 'const', 'csng', 'cstr', 'cvar',
  #                    'declare', 'defbool', 'defbyte', 'defdate', 'defdouble', 'defint', 'deflng', 'deflnglng',
  #                    'deflngptr', 'defobj', 'defsng', 'defstr', 'dim', 'do', 'double', 'each', 'elseif', 'empty',
  #                    'end', 'enum', 'erase', 'error', 'event', 'exit', 'explicit', 'function', 'get', 'goto',
  #                    'implements', 'integer', 'is', 'let', 'lbound', 'lib', 'like','long', 'longlong', 'loop', 'lset',
  #                    'me', 'mod', 'new', 'next', 'not', 'nothing', 'null', 'object', 'on', 'option', 'optional',
  #                    'paramarray', 'preserve', 'private', 'property', 'public', 'raiseevent', 'redim', 'resume',
  #                    'rset', 'select', 'set', 'single', 'static', 'step', 'stop', 'string', 'sub', 'then',
  #                    'to', 'true', 'type', 'typeof', 'ubound', 'until', 'wend', 'while', 'with', 'withevents'})
  # # ignore Java keywords
  # stop_words.update({'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'continue',
  #                    'default', 'do', 'double', 'else', 'enum', 'exports', 'extends', 'final', 'finally', 'float',
  #                    'for', 'if', 'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'module', 'native',
  #                    'new', 'package', 'private', 'protected', 'public', 'requires', 'short', 'static',
  #                    'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws', 'transient', 'try',
  #                    'void', 'volatile', 'while', 'true', 'null', 'false', 'var', 'const', 'goto'})
  # # ignore C keywords
  # stop_words.update({'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
  #                    'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'short', 'signed',
  #                    'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile',
  #                    'while'})
  # ignore common constants
  stop_words.update({'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'})
  return stop_words


def index_monthly_word_frequencies(spark_session, sql_context, start_date, end_date):
  """
  method name explains itself
  :param spark_session: for freeing memory
  :param sql_context: spark sql context
  :param start_date: datetime
  :param end_date: datetime
  :return: None
  """
  stop_words = create_stop_words()
  start_date = start_date.replace(day=1)
  for n in range((end_date.year - start_date.year) * 12 + end_date.month - start_date.month):
    month = start_date + relativedelta(months=+n)
    print(month)
    frequencies = word_frequencies_for_month(sql_context, month, stop_words)
    date_appended_frequencies = frequencies.withColumn("date", functions.lit(month - timedelta(hours=4)))
    frequencies.unpersist()
    insert_df_to_table(date_appended_frequencies, "word_frequencies")
    date_appended_frequencies.unpersist()
    spark_session.catalog.clearCache()
  return


def get_post_site_size(sql_context, start_date, end_date):
  """
  method name explains itself
  :param sql_context: spark sql
  :param start_date: starting datetime, string
  :param end_date: ending datetime, string
  :return: a spark_session data frame, starts and ends four hours early relative to queried datetime range
  """
  query = "SELECT siteId, LENGTH(body) as size " + \
          "FROM " + SCHEMA + ".post " + \
          "WHERE dateCreated BETWEEN \"" + \
          start_date + "\" AND \"" + end_date + "\""
  return execute_query(sql_context, query)


def sum_post_size_by_site(df):
  """
  aggregates the size of the posts by sites
  :param df: dataframe containing siteId and postSize, will be freed
  :return: aggregated df
  """
  summed = df.groupBy('siteId').agg(functions.sum('size')).withColumnRenamed('sum(size)','size')
  df.unpersist()
  return summed


def index_hourly_post_sizes(sql_context, start, hourly_offset):
  current = start + relativedelta(hours=+hourly_offset)
  print(current)
  sizes = get_post_site_size(sql_context, offset_time_string(current), offset_time_string(current  + relativedelta(hours=+1)))
  total_post_sizes = sum_post_size_by_site(sizes)
  date_appended_sizes = total_post_sizes.withColumn("time", functions.lit(current - timedelta(hours=4)))
  total_post_sizes.unpersist()
  insert_df_to_table(date_appended_sizes, "hourly_post_sizes")
  date_appended_sizes.unpersist()
  return


def index_all_hourly_total_post_sizes(spark_session, sql_context, start_date, end_date):
  """
  method name explains itself
  :param spark_session: for freeing memory
  :param sql_context: spark sql context
  :param start_date: datetime
  :param end_date: datetime
  :return: None
  """
  diff = end_date - start_date
  days_apart, seconds_apart = diff.days, diff.seconds
  hours_apart = days_apart * 24 + seconds_apart // 3600

  with ThreadPoolExecutor(max_workers=500) as executor:
    offsets = range(hours_apart)
    [executor.submit(index_hourly_post_sizes, sql_context, start_date, n) for n in offsets]
  return

def perform_sentiment_anlysis_helper(post):
  sentiment = TextBlob(post.body).sentiment
  return (post.postId, post.siteId, sentiment.polarity, sentiment.subjectivity)

def perform_sentiment_analysis(sql_context, start_date, end_date):
  posts = get_post_site_text(sql_context, start_date, end_date)
  posts_cleaned = posts.withColumn("body", spark_function_clean_string(functions.column('body')))
  posts.unpersist()
  sentiment_values = posts_cleaned.rdd.map(lambda x:  perform_sentiment_anlysis_helper(x))
  insert_df_to_table(sentiment_values.toDF(["postId", "siteId", "polarity", "subjectivity"]), "sentiment_values")
  sentiment_values.unpersist()

def date_range(start_date, end_date):
  counter_date = start_date
  while start_date < end_date:
    yield start_date
    start_date += timedelta(days=1)

def main():
  spark_session = SparkSession \
    .builder \
    .appName("Database access example") \
    .config('spark.driver.extraClassPath', './mysql-connector-java-8.0.16.jar') \
    .config('spark.executor.memory', '450g') \
    .config('spark.driver.memory', '450g') \
    .config('spark.executor.cores', '45') \
    .config('spark.cores.max', '45') \
    .getOrCreate()
  # spark_session = SparkSession \
  #   .builder \
  #   .appName("Database access example") \
  #   .config('spark.driver.extraClassPath', './mysql-connector-java-8.0.16.jar') \
  #   .getOrCreate()
  sc = spark_session.sparkContext
  sc.setLogLevel("WARN")
  sql_context = SQLContext(sc)

  # start_date = get_first_post_time(sql_context).collect()[0]['dateCreated'].replace(minute=0, second=0)
  # end_date = get_last_post_time(sql_context).collect()[0]['dateCreated'].replace(minute=0, second=0)
  # start_date = end_date + relativedelta(years=-1)
  # index_all_hourly_total_post_sizes(spark_session, sql_context, start_date, end_date)

  start_date = datetime.strptime("2018-01-03", "%Y-%m-%d")
  end_date = datetime.strptime("2018-03-15", "%Y-%m-%d")

  for dt in date_range(start_date, end_date):
      print(dt)
      perform_sentiment_analysis(sql_context, offset_time_string(dt), offset_time_string(dt + timedelta(days=1, microseconds=-1)))

if __name__ == "__main__":
  main()
