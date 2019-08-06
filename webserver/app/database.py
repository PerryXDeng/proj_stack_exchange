# mysql
import mysql.connector
import creds
# data mangling
import pandas.io.sql as psql


def query(statement):
  """
  establishes a connection and makes a query
  :param statement: sql
  :return: pandas data frame
  """
  conn = mysql.connector.connect(user=creds.USERNAME, password=creds.PASSWORD,
                                 host='127.0.0.1', database=creds.SCHEMA)
  df = psql.read_sql_query(statement, conn)
  conn.close()
  return df


def get_site_name(siteId):
  """
  get the name of the site given a siteId
  :param siteId: int
  :return: string
  """
  df = query("SELECT name FROM site WHERE siteId=" + str(siteId))
  return df['name'].values[0]
