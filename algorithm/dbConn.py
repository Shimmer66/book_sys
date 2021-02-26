import MySQLdb
import pandas as pd


conn = MySQLdb.connect(host='127.0.0.1',
                       port=3306,
                       user='root',
                       passwd='why..219',
                       db='book_master',
                       charset='utf8')

def booksGet():
    sql1 = 'SELECT * FROM `user_book`;'
    books = pd.read_sql(sql1, conn)
    return books

def ratings_explicitGet():
    sql2 = 'SELECT * FROM `RatingsExplicit`'
    ratings_explicit = pd.read_sql(sql2, conn)
    return ratings_explicit

def ratings_implicitGet():
    sql3 = 'SELECT * FROM `RatingsImplicit`'
    ratings_implicit = pd.read_sql(sql3, conn)
    return ratings_implicit

def users_exp_ratingsGet():
    sql4 = 'SELECT * FROM `users_exp_ratings`'
    users_exp_ratings = pd.read_sql(sql4, conn)
    return users_exp_ratings

def users_imp_ratingsGet():
    sql5 = 'SELECT * FROM `users_imp_ratings`'
    users_imp_ratings = pd.read_sql(sql5, conn)
    return users_imp_ratings

def first_indexGet():
    sql6 = 'SELECT * FROM `ratings_matrix_user`'
    first_list = pd.read_sql(sql6, conn)
    return first_list
