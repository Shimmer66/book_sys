import numpy as np
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import re

# from getUserId import UseridGet
from algorithm.ratingmatrix import dealmatrix
from algorithm.dbConn import booksGet

# 函数findksimilarusers输入用户ID和评分矩阵，并返回k个相似用户的相似度和指数。
def findkUsersimilarusers(user_id, ratings, metric='cosine', k=10):
    similarities = []
    indices = []
    model_knn = NearestNeighbors(metric=metric, algorithm='brute')
    model_knn.fit(ratings)
    loc = ratings.index.get_loc(user_id)
    distances, indices = model_knn.kneighbors(ratings.iloc[loc, :].values.reshape(1, -1), n_neighbors=k + 1)
    similarities = 1 - distances.flatten()

    return similarities, indices


# 函数predict_userbased基于用户的方法对特定的user-item组合进行评分
def predict_userbased(user_id, item_id, ratings, metric='cosine', k=10):
    prediction = 0
    user_loc = ratings.index.get_loc(user_id)
    item_loc = ratings.columns.get_loc(item_id)
    similarities, indices = findkUsersimilarusers(user_id, ratings, metric, k)  # similar users based on cosine similarity
    mean_rating = ratings.iloc[user_loc, :].mean()  # to adjust for zero based indexing
    sum_wt = np.sum(similarities) - 1
    product = 1
    wtd_sum = 0

    for i in range(0, len(indices.flatten())):
        if indices.flatten()[i] == user_loc:
            continue;
        else:
            ratings_diff = ratings.iloc[indices.flatten()[i], item_loc] - np.mean(ratings.iloc[indices.flatten()[i], :])
            product = ratings_diff * (similarities[i])
            wtd_sum = wtd_sum + product

    # in case of very sparse datasets, using correlation metric for collaborative based approach may give negative ratings
    # which are handled here as below
    if prediction <= 0:
        prediction = 1
    elif prediction > 10:
        prediction = 10

    prediction = int(round(mean_rating + (wtd_sum / sum_wt)))
    # print('\nPredicted rating for mysite {0} -> item {1}: {2}'.format(user_id, item_id, prediction))

    return prediction

def recommendItemU(user_id, ratings, books,metric='cosine'):
    isbn = []
    if (user_id not in ratings.index.values):

    # if (user_id not in ratings.index.values) or type(user_id) is not int:
        print ("User id should be a valid integer from this list :\n\n {} ".format(re.sub('[\[\]]', '', np.array_str(ratings.index.values))))
    else:
        prediction = []
        for i in range(ratings.shape[1]):
            if (ratings[str(ratings.columns[i])][user_id] !=0): #not rated already
                prediction.append(predict_userbased(user_id, str(ratings.columns[i]) ,ratings, metric))
            else:
                prediction.append(-1) #for already rated items
        prediction = pd.Series(prediction)
        prediction = prediction.sort_values(ascending=False)
        recommended = prediction[:10]
#         print ("As per {0} approach....Following books are recommended...".format(select.value))
        for i in range(len(recommended)):
            isbn.append(books.ISBN[recommended.index[i]])
        return isbn

def UserBased(user_id):
    books = booksGet()
    # user_id = '2033'
    ratings = dealmatrix()
    ISBN = recommendItemU(user_id=user_id,ratings=ratings,books=books)
    return ISBN





