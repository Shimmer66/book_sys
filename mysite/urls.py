from django.urls import path, include
from mysite import views

urlpatterns = [
    path("",views.homepage,name="home"),
    path("index", views.all_book, name="index"),  # 所有书籍
    path("login/", views.login, name="login"),  # 登录
    path("register/", views.register, name="register"),  # 注册
    path("logout/", views.logout, name="logout"),  # 退出
    # path("item/", views.item, name="item"),
    path("all_book/", views.all_book, name="all_book"),  # 所有书籍
    path("book/<int:book_id>/", views.book, name="book"),  # 具体的书籍

    path("score/<int:book_id>/", views.score, name="score"),  # 评分
    path("comment/<int:book_id>/", views.commen, name="comment"),  # 评论
    path("good/<int:commen_id>/<int:book_id>/", views.good, name="good"),  # 给评论内容点赞
    path("collect/<int:book_id>/", views.collect, name="collect"),  # 收藏
    path("decollect/<int:book_id>/", views.decollect, name="decollect"),  # 取消
    path("message_boards/<int:fap_id>/<int:pagenum>/", views.message_boards, name="message_boards"),  # 获取论坛
    path("get_message_board/<int:message_board_id>/<int:fap_id>/<int:currentpage>/", views.get_message_board,
         name="get_message_board"),  # 获取论坛详情
    path("new_board_comment/<int:message_board_id>/<int:fap_id>/<int:currentpage>/", views.new_board_comment,
         name="new_board_comment"),  # 发表论坛评论
    path("new_message_board/", views.new_message_board, name="new_message_board"),  # 发表论坛
    path("like_collect/", views.like_collect, name="like_collect"),  # 对论坛留言点赞或收藏

    path("personal/", views.personal, name="personal"),  # 获取我的信息
    path("mycollect/", views.mycollect, name="mycollect"),  # 获取我的收藏
    path("myinfo/", views.myinfo, name="myinfo"),  # 修改我的个人信息
    path("myfoot/", views.myfoot, name="myfoot"),  # 获取我的足迹
    path("myjoin/", views.myjoin, name="myjoin"),  # 我参加的活动
    path("my_comments/", views.my_comments, name="my_comments"),  # 我的评论
    path("my_rate/", views.my_rate, name="my_rate"),  # 我打分过的书籍
    path("delete_comment/<int:comment_id>", views.delete_comment, name="delete_comment"),  # 取消评论
    path("delete_rate/<int:rate_id>", views.delete_rate, name="delete_rate"),  # 取消评分
    path("hot_book/", views.hot_book, name="hot_book"),  # 获取热门书籍
    path("latest_book/", views.latest_book, name="latest_book"),  # 获取最新的书籍
    path("search/", views.search, name="search"),  # 搜索

    path("begin/", views.begin, name="begin"),  # 开始
    path("week_reco/", views.reco_by_item, name="week_reco"),  # 物品推荐
    # path("item_reco/", views.reco_by_item, name="item_reco"),  # 基于物品推荐
    path("user_reco/", views.reco_by_user, name="user_reco"),  # 基于用户推荐
    path("cold_boot/", views.cold_boot, name="cold_boot"),  # 冷启动
    path("svd/", views.svd, name="svd"),  # SVD

]
