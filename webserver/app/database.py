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
