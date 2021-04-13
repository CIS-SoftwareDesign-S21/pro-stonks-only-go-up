import mysql.connector
from mysql.connector import errorcode
import databaseconfig as config


def __exec(stmt, args):
    try:
        cnx = mysql.connector.connect(**config.mysql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cursor = cnx.cursor()
        try:
            cursor.execute(stmt, args)
        except mysql.connector.Error as err:
            print(err)
        result = cursor.fetchall() # might cause problems if fetching a lot of data?
        cursor.close()
        cnx.close()
        return result
        

def insert_reddit_post(ticker, title, content): 
    __exec(("INSERT INTO reddit_post "
            "(post_ticker, post_title, post_content) "
            "VALUES (%s, %s)"),
            (ticker.upper(), title, content))

def insert_twitter_post(ticker, content):
    __exec(("INSERT INTO twitter_post "
            "(post_ticker, post_content) "
            "VALUES (%s, %s)"),
            (ticker.upper(), content))

def get_reddit_posts(ticker):
    return __exec(("SELECT post_title, post_content FROM reddit_post "
                    "WHERE post_ticker = %s"),
                    (ticker.upper(), ))

def get_twitter_posts(ticker):
    return __exec(("SELECT post_content FROM twitter_post "
                    "WHERE post_ticker = %s"),
                    (ticker.upper(), ))