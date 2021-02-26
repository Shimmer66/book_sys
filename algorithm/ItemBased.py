import numpy as np
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import re

# from getUserId import UseridGet
from algorithm.ratingmatrix import dealmatrix
from algorithm.dbConn import booksGet


# 为基于item的CF编写了类似的函数，可以找到k本类似的书籍，并预测每本书的用户评分。
# 相同的函数recommendItem可用于基于item的方法和选定的度量标准推荐图书。
# 如果图书的预测评分大于或等于6，并且图书尚未被评分，则进行推荐。

def findksimilaritems(item_id, ratings, metric='cosine', k=10):
    similarities = []
    indices = []
    ratings = ratings.T
    loc = ratings.index.get_loc(item_id)
    model_knn = NearestNeighbors(metric=metric, algorithm='brute')
    model_knn.fit(ratings)

    distances, indices = model_knn.kneighbors(ratings.iloc[loc, :].values.reshape(1, -1), n_neighbors=k + 1)
    similarities = 1 - distances.flatten()

    return similarities, indices


def predict_itembased(user_id, item_id, ratings, metric='cosine', k=10):
    prediction = wtd_sum = 0
    user_loc = ratings.index.get_loc(user_id)
    item_loc = ratings.columns.get_loc(item_id)
    similarities, indices = findksimilaritems(item_id, ratings)  # similar users based on correlation coefficients
    sum_wt = np.sum(similarities) - 1
    product = 1
    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i] == item_loc:
            continue;
        else:
            product = ratings.iloc[user_loc, indices.flatten()[i]] * (similarities[i])
            wtd_sum = wtd_sum + product
    prediction = int(round(wtd_sum / sum_wt))

    # in case of very sparse datasets, using correlation metric for collaborative based approach may give negative ratings
    # which are handled here as below //code has been validated without the code snippet below, below snippet is to avoid negative
    # predictions which might arise in case of very sparse datasets when using correlation metric
    if prediction <= 0:
        prediction = 1
    elif prediction > 10:
        prediction = 10

    # print('\nPredicted rating for mysite {0} -> item {1}: {2}'.format(user_id, item_id, prediction))

    return prediction

def recommendItemI(user_id, ratings, books,metric='cosine'):
    isbn = []
    if (user_id not in ratings.index.values) :
        print ("User id should be a valid integer from this list :\n\n {} ".format(re.sub('[\[\]]', '', np.array_str(ratings.index.values))))
    else:
        prediction = []
        for i in range(ratings.shape[1]):
            if (ratings[str(ratings.columns[i])][user_id] !=0): #not rated already
                prediction.append(predict_itembased(user_id, str(ratings.columns[i]) ,ratings, metric))
            else:
                prediction.append(-1) #for already rated items
        prediction = pd.Series(prediction)
        prediction = prediction.sort_values(ascending=False)
        recommended = prediction[:10]
        # print ("As per {0} approach....Following books are recommended...".format(select.value))
        for i in range(len(recommended)):
            isbn.append(books.ISBN[recommended.index[i]])
        return isbn

def ItemBased(user_id):
    books = booksGet()
    # user_id = '2033'
    ratings = dealmatrix()
    ISBN = recommendItemI(user_id=user_id,ratings=ratings,books=books)
    return ISBN
