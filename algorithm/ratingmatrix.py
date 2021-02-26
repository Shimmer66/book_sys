from algorithm.dbConn import ratings_explicitGet
import numpy as np

## 用户-评分矩阵
# 为了配合机器的计算能力并减少数据集大小，我们选择至少对100本书籍
# 进行打分的用户，以及至少有100个评分的书籍
def create_ratings_matrix(ratings_explicit):
    counts1 = ratings_explicit['userID'].value_counts()
    ratings_explicit = ratings_explicit[ratings_explicit['userID'].isin(counts1[counts1 >= 100].index)]
    counts = ratings_explicit['bookRating'].value_counts()
    ratings_explicit = ratings_explicit[ratings_explicit['bookRating'].isin(counts[counts >= 100].index)]

    # 构建基于CF的推荐系统的下一个关键步骤是从评分表中生成用户-项目评分矩阵。
    ratings_matrix = ratings_explicit.pivot(index='userID', columns='ISBN', values='bookRating')
    userID = ratings_matrix.index
    ISBN = ratings_matrix.columns
    # print(ratings_matrix.shape)
    ratings_matrix.fillna(0, inplace=True)
    ratings_matrix = ratings_matrix.astype(np.int32)
    # print(ratings_matrix.head())
    return ratings_matrix

def dealmatrix():
    ratings_explicit = ratings_explicitGet()
    ratings_matrix = create_ratings_matrix(ratings_explicit)
    return ratings_matrix
