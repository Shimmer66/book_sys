from algorithm.ratingmatrix import dealmatrix
from algorithm.dbConn import first_indexGet

import numpy as np

## 矩阵分解
def ISBNGet(ratings_matrix):
    # 对于用于-评分矩阵的数据处理
    ISBN = ratings_matrix.columns
    bianhao = list(ISBN)
    del bianhao[0]
    return bianhao

# def dataHandle(ratings_matrix):
#     foo = np.array(ratings_matrix)
#     datan = foo
#     first_list = datan[:, 0]
#     first_list = list(first_list)
#     # first_list = [str(j) for j in first_list]
#     # data = np.delete(datan, 0, 1)  # 删除第一列
#     return datan,first_list
def chuli(first_list):
    first_list = list(first_list['userID'])
    first_list = [str(j) for j in first_list]
    return first_list

def recommendLFM(userID,lr,alpha,d,n_iter,data,first_list,bianhao):
    '''
    userID(int):推荐用户ID
    lr(float):学习率
    alpha(float):权重衰减系数
    d(int):矩阵分解因子(即元素个数)
    n_iter(int):训练轮数
    data(ndarray):用户-电影评分矩阵
    '''
    # first_list = list(first_list['userID'])
    # first_list = [str(j) for j in first_list]

    #获取用户数与电影数
    m,n = data.shape
    #初始化参数
    x = np.random.uniform(0,1,(m,d))
    w = np.random.uniform(0,1,(d,n))
    #创建评分记录表，无评分记为0，有评分记为1
    record = np.array(data>0,dtype=int)
    #梯度下降，更新参数
    for i in range(n_iter):
        x_grads = np.dot(np.multiply(record,np.dot(x,w)-data),w.T)
        w_grads = np.dot(x.T,np.multiply(record,np.dot(x,w)-data))
        x = alpha*x - lr*x_grads
        w = alpha*w - lr*w_grads
    #预测
    predict = np.dot(x,w)
    id = first_list.index(userID)
    # 将用户未看过的电影分值从低到高进行排列
    for i in range(n):
        if record[id][i] == 1 :
            predict[id][i] = 0
    recommend = np.argsort(predict[id])
    a = recommend[-1]
    b = recommend[-2]
    c = recommend[-3]
    d = recommend[-4]
    e = recommend[-5]
    f = recommend[-6]
    g = recommend[-7]
    h = recommend[-8]
    i = recommend[-9]
    j = recommend[-10]
    # print('为用户%s推荐的图书ISBN为：\n1:%s\n2:%s\n3:%s\n4:%s\n5:%s。'% (userID, bianhao[a], bianhao[b], bianhao[c], bianhao[d], bianhao[e]))
    l = []
    l.append(bianhao[a])
    l.append(bianhao[b])
    l.append(bianhao[c])
    l.append(bianhao[d])
    l.append(bianhao[e])
    l.append(bianhao[f])
    l.append(bianhao[g])
    l.append(bianhao[h])
    l.append(bianhao[i])
    l.append(bianhao[j])
    return l

def SVDGet(user_id):
    lr = 1e-4
    alpha=0.999
    d=20
    n_iter=10
    data = dealmatrix()
    first_list = chuli(first_indexGet())
    bianhao = ISBNGet(data)
    ISBN = recommendLFM(userID=user_id, lr=1e-4, alpha=0.999, d=d, n_iter=n_iter, data=data, first_list=first_list,
                 bianhao=bianhao)
    return ISBN
