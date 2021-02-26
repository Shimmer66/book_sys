import pandas as pd
from algorithm.dbConn import ratings_explicitGet,booksGet

def Simple_Popularity(ratings_explicit,books):
    ratings_count = pd.DataFrame(ratings_explicit.groupby(['ISBN'])['bookRating'].sum())
    top10 = ratings_count.sort_values('bookRating', ascending = False).head(10)
    # print("Following books are recommended")
    # print(top10.merge(books, left_index = True, right_on = 'ISBN'))
    result = top10.merge(books, left_index = True, right_on = 'ISBN')
    return result
def lengqidong():
    books = booksGet()
    ratings_explicit = ratings_explicitGet()
    result = Simple_Popularity(ratings_explicit,books)
    # 此处result为dataframe类型
    # 取出ISBN列
    # 将数据转换成列表
    ISBN = result['ISBN']
    ISBN = list(ISBN)
    # 返回书籍ISBN编码
    return ISBN
