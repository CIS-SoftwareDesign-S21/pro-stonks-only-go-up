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
        try:
            result = cursor.fetchall()
            cursor.close()
            cnx.close()
            return result
        except mysql.connector.Error as err:
            print(err)
        else:
            cursor.close()
            cnx.close()
        

def insert_reddit_post(ticker, title, content, date, sentiment): 
    __exec(("INSERT INTO reddit_post "
            "(post_ticker, post_title, post_content, post_date, post_sentiment) "
            "VALUES (%s, %s, %s, %s, %s) "
            "ON DUPLICATE KEY UPDATE post_sentiment = %s"),
            (ticker.upper(), title, content, date, sentiment, sentiment))

def insert_twitter_post(ticker, content, date, sentiment):
    __exec(("INSERT INTO twitter_post "
            "(post_ticker, post_content, post_date, post_sentiment) "
            "VALUES (%s, %s, %s, %s) "
            "ON DUPLICATE KEY UPDATE post_sentiment = %s"),
            (ticker.upper(), content, date, sentiment, sentiment))

def get_reddit_posts(ticker, end_date=None):
    if not end_date:
        end_date = '0000-00-00'
    return __exec(("SELECT post_title, post_content, post_date, post_sentiment FROM reddit_post "
                    "WHERE post_ticker = %s and post_date >= %s ORDER BY post_date DESC"),
                    (ticker.upper(), end_date))

def get_twitter_posts(ticker, end_date=None):
    if not end_date:
        end_date = '0000-00-00'
    return __exec(("SELECT post_content, post_date, post_sentiment FROM twitter_post "
                    "WHERE post_ticker = %s and post_date >= %s ORDER BY post_date DESC"),
                    (ticker.upper(), end_date))