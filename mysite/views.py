import datetime
from functools import wraps


from django.core.paginator import Paginator
from django.db.models import Q, Count, F, Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.renderers import JSONRenderer

#算法

from algorithm.ItemBased import ItemBased
from algorithm.Popularity import lengqidong
from algorithm.UserBased import UserBased
from algorithm.SVD import SVDGet
#算法

from .forms import *

def homepage(request):
    return render(
        request, "index.html"    )
    pass



def login_in(func):  # 验证用户是否登录
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = args[0]
        is_login = request.session.get("login_in")
        if is_login:
            return func(*args, **kwargs)
        else:
            return redirect(reverse("login"))

    return wrapper


def books_paginator(books, page):
    paginator = Paginator(books, 6)  # 拿到分页器对象，第一个参数：对象列表，第二个参数：每页显示的条数
    if page is None:
        page = 1
    books = paginator.page(page)
    return books


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs["content_type"] = "application/json"
        super(JSONResponse, self).__init__(content, **kwargs)


def login(request):
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            result = User.objects.filter(username=username)
            if result:
                user = User.objects.get(username=username)
                if user.password == password:
                    request.session["login_in"] = True
                    request.session["user_id"] = user.id
                    request.session["name"] = user.name
                    return redirect(reverse("all_book"))
                else:
                    return render(
                        request, "login.html", {"form": form, "error": "账号或密码错误"}
                    )
            else:
                return render(
                    request, "login.html", {"form": form, "error": "账号不存在"}
                )
    else:
        form = Login()
        return render(request, "login.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        error = None
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password2"]
            email = form.cleaned_data["email"]
            name = form.cleaned_data["name"]
            phone = form.cleaned_data["phone"]

            User.objects.create(
                username=username,
                password=password,
                email=email,
                name=name,
                phone=phone,

            )
            # 根据表单数据创建一个新的用户
            return redirect(reverse("login"))  # 跳转到登录界面
        else:
            # print(form, 'lllllllllllllllll')
            return render(
                request, "register.html", {"form": form, "error": error}
            )  # 表单验证失败返回一个空表单到注册页面
    form = RegisterForm()
    return render(request, "register.html", {"form": form})


def logout(request):
    if not request.session.get("login_in", None):  # 不在登录状态跳转回首页
        return redirect(reverse("index"))
    request.session.flush()  # 清除session信息
    return redirect(reverse("index"))


def all_book(request):
    # aggregate返回的是一个字典，在这个字典中存储的是这个聚合函数执行的结果。而annotate返回的是一个QuerySet对象，并且会在查找的模型上添加一个聚合函数的属性。
    # aggregate不会做分组，而annotate会使用group
    # by子句进行分组，只有调用了group
    # by子句，才能对每一条数据求聚合函数的值

    books = Book.objects.annotate(user_collector=Count('collect')).order_by('-user_collector')

    print("all_book")
    # test
    print(books)
    print("all_book")
    paginator = Paginator(books, 9)
    current_page = request.GET.get("page", 1)
    # print(current_page)
    books = paginator.page(current_page)
    print(books)
    return render(request, "item.html", {"books": books, "title": "所有书籍"})



def search(request):  # 搜索
    if request.method == "POST":  # 如果搜索界面
        key = request.POST["search"]
        request.session["search"] = key  # 记录搜索关键词解决跳页问题
    else:
        key = request.session.get("search")  # 得到关键词
    books = Book.objects.filter(
        Q(title__icontains=key) | Q(yearofpublication__contains=key) | Q(author__icontains=key)
    )  # 进行内容的模糊搜索
    page_num = request.GET.get("page", 1)
    books = books_paginator(books, page_num)
    return render(request, "item.html", {"books": books})
@login_in
def book(request, book_id):  #浏览量  用户足迹
    # 获取具体的书籍
    book = Book.objects.get(pk=book_id) #pk 主碼
    user = User.objects.get(id=request.session.get("user_id"))#获取当前登录用户
    print(user.username)
    now_data = datetime.datetime.now()
    user_id=request.session.get("user_id")
    url=request.path_info
    print("url",url)
    url="127.0.0.1:8000"+url
    print(url)
    #test
    bool_info=MyFootprint.objects.filter(Q(user_id=user_id) & Q(book_id=book_id))
    # print(bool_info)
    # if (bool_info.exists()):
    #     print("has data")
    # else:
    #     print("no data")
    if (bool_info.exists()):
# 保存 BUG
#         print(bool_info.create_time)
        Newdate=bool_info[0]
        print(now_data)
        Newdate.create_time=now_data
        # bool_info.age=5
        # print(bool_info.create_time)
        Newdate.save()


    else:
        Newdate=MyFootprint(user_id=user_id,book_id=book_id,username=user.username,bookname=book.title,url=url)
        Newdate.save()

    print(book.num)
    book.num += 1
    book.save()
    comments = book.comment_set.order_by("-create_time")
    user_id = request.session.get("user_id")
    rate = Rate.objects.filter(book=book).aggregate(Avg("mark")).get("mark__avg", 0)
    rate = rate if rate else 0
    book_rate = round(rate, 2)

    if user_id:
        user = User.objects.get(pk=user_id)
        is_collect = book.collect.filter(id=user_id).first()
        is_rate = Rate.objects.filter(book=book, user=user).first()
    rate_num = book.rate_num
    collector = book.collector
    return render(request, "book.html", locals()) #locals()返回的字典对所有局部变量的名称与值进行映射。


@login_in
def score(request, book_id):
    # 打分
    user = User.objects.get(id=request.session.get("user_id"))
    book = Book.objects.get(id=book_id)
    score = float(request.POST.get("score", 0))
    is_rate = Rate.objects.filter(book=book, user=user).first()
    if not is_rate:
        book.rate_num += 1
        book.save()
        Rate.objects.get_or_create(user=user, book=book, defaults={"mark": score})
        is_rate = {'mark': score}
    comments = book.comment_set.order_by("-create_time")
    user_id = request.session.get("user_id")
    rate = Rate.objects.filter(book=book).aggregate(Avg("mark")).get("mark__avg", 0)
    rate = rate if rate else 0
    book_rate = round(rate, 2)
    user = User.objects.get(pk=user_id)
    is_collect = book.collect.filter(id=user_id).first()
    rate_num = book.rate_num
    collector = book.collector
    return render(request, "book.html", locals())


@login_in
def commen(request, book_id):
    # 评论
    user = User.objects.get(id=request.session.get("user_id"))
    book = Book.objects.get(id=book_id)
    comment = request.POST.get("comment", "")
    Comment.objects.create(user=user, book=book, content=comment)
    comments = book.comment_set.order_by("-create_time")
    user_id = request.session.get("user_id")
    rate = Rate.objects.filter(book=book).aggregate(Avg("mark")).get("mark__avg", 0)
    rate = rate if rate else 0
    book_rate = round(rate, 2)
    user = User.objects.get(pk=user_id)
    is_collect = book.collect.filter(id=user_id).first()
    is_rate = Rate.objects.filter(book=book, user=user).first()
    rate_num = book.rate_num
    collector = book.collector
    return render(request, "book.html", locals())


@login_in
def good(request, commen_id, book_id):
    # 点赞
    commen = Comment.objects.get(id=commen_id)
    commen.good += 1
    commen.save()
    book = Book.objects.get(id=book_id)
    comments = book.comment_set.order_by("-create_time")
    user_id = request.session.get("user_id")
    rate = Rate.objects.filter(book=book).aggregate(Avg("mark")).get("mark__avg", 0)
    rate = rate if rate else 0
    book_rate = round(rate, 2)
    if user_id is not None:
        user = User.objects.get(pk=user_id)
        is_collect = book.collect.filter(id=user_id).first()
        is_rate = Rate.objects.filter(book=book, user=user).first()
    rate_num = book.rate_num
    collector = book.collector
    return render(request, "book.html", locals())


@login_in
def collect(request, book_id):
    user = User.objects.get(id=request.session.get("user_id"))
    book = Book.objects.get(id=book_id)
    book.collect.add(user)
    book.collector += 1  # 收藏人数加1
    book.save()

    comments = book.comment_set.order_by("-create_time")
    user_id = request.session.get("user_id")
    rate = Rate.objects.filter(book=book).aggregate(Avg("mark")).get("mark__avg", 0)
    rate = rate if rate else 0
    book_rate = round(rate, 2)

    user = User.objects.get(pk=user_id)
    is_collect = book.collect.filter(id=user_id).first()
    is_rate = Rate.objects.filter(book=book, user=user).first()
    rate_num = book.rate_num
    collector = book.collector
    return render(request, "book.html", locals())


@login_in
def decollect(request, book_id):
    user = User.objects.get(id=request.session.get("user_id"))
    book = Book.objects.get(id=book_id)
    book.collect.remove(user)
    book.collector -= 1
    book.save()
    comments = book.comment_set.order_by("-create_time")
    user_id = request.session.get("user_id")
    rate = Rate.objects.filter(book=book).aggregate(Avg("mark")).get("mark__avg", 0)
    rate = rate if rate else 0
    book_rate = round(rate, 2)

    user = User.objects.get(pk=user_id)
    is_collect = book.collect.filter(id=user_id).first()
    is_rate = Rate.objects.filter(book=book, user=user).first()
    rate_num = book.rate_num
    collector = book.collector
    return render(request, "book.html", locals())



# @cache_page(60 * 1)
def message_boards(request, fap_id=1, pagenum=1, **kwargs):
    # 获取论坛内容
    msg = request.GET.get('msg', '')
    # print('做了缓存')
    have_board = True
    if fap_id == 1:
        # 热门
        msg_board = Messageboard.objects.all().order_by('-like_num')
    elif fap_id == 2:
        # 最新
        msg_board = Messageboard.objects.all().order_by('-create_time')
    elif fap_id == 3:
        # 点赞
        is_login = request.session.get("login_in")
        if not is_login:
            return redirect(reverse("login"))
        user = User.objects.get(id=request.session.get("user_id"))
        collectboards = Collectboard.objects.filter(user=user, is_like=True).order_by(
            'create_time')
        msg_board = []
        for mb in collectboards:
            msg_board.append(mb.message_board)

    elif fap_id == 4:
        # 收藏
        is_login = request.session.get("login_in")
        if not is_login:
            return redirect(reverse("login"))
        user = User.objects.get(id=request.session.get("user_id"))
        collectboards = Collectboard.objects.filter(user=user, is_collect=True).order_by(
            'create_time')
        msg_board = []
        for mb in collectboards:
            msg_board.append(mb.message_board)
    elif fap_id == 5:
        # 我的
        is_login = request.session.get("login_in")
        if not is_login:
            return redirect(reverse("login"))
        user = User.objects.get(id=request.session.get("user_id"))
        msg_board = Messageboard.objects.filter(user=user).order_by('-create_time')
    else:
        msg_board = Messageboard.objects.all().order_by('create_time')
    if not msg_board:
        have_board = False

    # 构建分页器对象,blogs=所有博文,2=每页显示的个数
    paginator = Paginator(msg_board, 10)

    # 获取第n页的页面对象
    page = paginator.page(pagenum)

    # Paginator和Page的常用API
    # page.previous_page_number()
    # page.next_page_number()
    # page.has_previous()
    # page.has_next()

    # 构造页面渲染的数据
    '''
    渲染需要的数据:
    - 当前页的博文对象列表
    - 分页页码范围
    - 当前页的页码
    '''
    data = {
        # 当前页的博文对象列表
        "page": page,
        # 分页页码范围
        "pagerange": paginator.page_range,
        # 当前页的页码
        "currentpage": page.number,
        "message_boards": msg_board,
        "have_board": have_board,
        "fap_id": fap_id,
    }

    return render(request, "message_boards.html", context=data)


@login_in
def new_message_board(request):
    # 写新论坛
    user = User.objects.get(id=request.session.get("user_id"))
    title = request.POST.get("title")
    content = request.POST.get("content")
    # print('ddddddddddddddddd', title, content)
    if not title or not content:
        return redirect(reverse("message_boards", kwargs={'fap_id': 2, 'pagenum': 1}))
    Messageboard.objects.create(user=user, content=content, title=title)
    return redirect(reverse("message_boards", args=(2, 1)))


def get_message_board(request, message_board_id, fap_id=1, currentpage=1):
    # 用户每浏览一次，就增加一次浏览量
    try:
        user = User.objects.get(id=request.session.get("user_id"))
        collectboard = Collectboard.objects.filter(user=user, message_board_id=message_board_id)
        is_like = collectboard.first().is_like
        is_collect = collectboard.first().is_collect
    except:
        is_like = 0
        is_collect = 0

    Messageboard.objects.filter(id=message_board_id).update(look_num=F('look_num') + 1)
    msg_board = Messageboard.objects.get(id=message_board_id)

    board_comments = msg_board.boardcomment_set.all()
    have_comment = True
    if not board_comments:
        have_comment = False

    context = {"msg_board": msg_board,
               "board_comments": board_comments,
               "have_comment": have_comment,
               "fap_id": fap_id,
               "currentpage": currentpage,
               'is_like': is_like,
               'is_collect': is_collect,
               'message_board_id': message_board_id
               }
    return render(request, "message_board.html", context=context)


@login_in
def new_board_comment(request, message_board_id, fap_id=1, currentpage=1):
    # 写评论
    content = request.POST.get("content")
    if not content:
        return redirect(reverse("get_message_board", args=(message_board_id, fap_id, currentpage)))

    Messageboard.objects.get(id=message_board_id)
    user = User.objects.get(id=request.session.get("user_id"))

    Boardcomment.objects.create(
        user=user, content=content, message_board_id=message_board_id
    )
    Messageboard.objects.filter(id=message_board_id).update(feebback_num=F('feebback_num') + 1)
    return redirect(reverse("get_message_board", args=(message_board_id, fap_id, currentpage)))


# @login_in
def like_collect(request):
    # 点赞或收藏

    try:
        user = User.objects.get(id=request.session.get("user_id"))
    except:
        return JsonResponse(data={'code': 2, 'msg': '没有登录'})
    message_board_id = request.POST.get("message_board_id")
    like_or_collect = request.POST.get("like_or_collect", None)  # 点赞还是收藏
    is_like = request.POST.get("is_like", None)  # 是否点赞
    is_collect = request.POST.get("is_collect", None)  # 是否收藏
    # print('lllll', like_or_collect, is_like, is_collect)
    if like_or_collect not in ['like', 'collect'] or None in [is_like, is_collect]:
        return JsonResponse(data={'code': 0, 'msg': '参数有误1'})
    try:
        collectboard = Collectboard.objects.filter(user=user, message_board_id=message_board_id)
        if not collectboard:
            Collectboard.objects.create(user=user, message_board_id=message_board_id,
                                        is_collect=is_collect if like_or_collect == 'collect' else 0,
                                        is_like=is_like if like_or_collect == 'like' else 0)
            if like_or_collect == 'like':
                if is_like == 0:
                    Messageboard.objects.filter(id=message_board_id).update(like_num=F('like_num') - 1)
                else:
                    Messageboard.objects.filter(id=message_board_id).update(like_num=F('like_num') + 1)
            else:
                if is_like == 0:
                    Messageboard.objects.filter(id=message_board_id).update(collect_num=F('collect_num') - 1)
                else:
                    Messageboard.objects.filter(id=message_board_id).update(collect_num=F('collect_num') + 1)
            return JsonResponse(data={'code': 1, 'msg': '操作成功'})
        collectboard = collectboard.first()
        if like_or_collect == 'like':
            is_collect = collectboard.is_collect
        else:
            is_like = collectboard.is_like
        Collectboard.objects.filter(user=user, message_board_id=message_board_id).update(is_collect=is_collect,
                                                                                         is_like=is_like)
        if like_or_collect == 'like':
            if is_like == 0:
                Messageboard.objects.filter(id=message_board_id).update(like_num=F('like_num') - 1)
            else:
                Messageboard.objects.filter(id=message_board_id).update(like_num=F('like_num') + 1)
        else:
            if is_like == 0:
                Messageboard.objects.filter(id=message_board_id).update(collect_num=F('collect_num') - 1)
            else:
                Messageboard.objects.filter(id=message_board_id).update(collect_num=F('collect_num') + 1)
        return JsonResponse(data={'code': 1, 'msg': '操作成功', 'is_like': is_like, 'is_collect': is_collect})
    except Exception as e:
        print(e)
        return JsonResponse(data={'code': 0, 'msg': '参数有误2'})


@login_in
def personal(request):
    # 获取我的信息

    user = User.objects.get(id=request.session.get("user_id"))
   # print(mysite)   #test

    #print(request.mysite)
    if request.method == "POST":
        form = Edit(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("personal"))
        else:
            return render(
                request, "personal.html", {"message": "修改失败", "form": form}
            )
    form = Edit(instance=user)
    return render(request, "personal.html", {"form": form,"user":user})
# request:　用于生成响应的请求对象
# template_name:　要使用的模板的完整名称, 可选的参数
# context:　添加到模板上下文的一个字典. 默认是一个空字典. 如果字典中的某个值是可调用的, 视图将在渲染模板之前调用它.
# content_type:　 生成的文档要使用的MIME类型. 默认为DEFAULT_CONTENT_TYPE设置的值. 默认为"texthtml"
# status:　响应的状态码. 默认为200
# useing:　用于加载模板的模板引擎的名称


@login_in
def mycollect(request):
    user = User.objects.get(id=request.session.get("user_id"))
    book = user.book_set.all()
    return render(request, "mycollect.html", {"book": book})


@login_in
def myjoin(request):
    user_id = request.session.get("user_id")
    user = User.objects.get(id=user_id)
    user_actions = user.action_set.all()
    return render(request, "myaction.html", {"action": user_actions})


@login_in
def my_comments(request):
    user = User.objects.get(id=request.session.get("user_id"))
    comments = user.comment_set.all()
    # print('comment:', comments)
    return render(request, "my_comment.html", {"comments": comments})


@login_in
def delete_comment(request, comment_id):
    # 删除评论
    Comment.objects.get(pk=comment_id).delete()
    user = User.objects.get(id=request.session.get("user_id"))
    comments = user.comment_set.all()
    # print('comment:', comments)
    return render(request, "my_comment.html", {"comments": comments})


@login_in
def my_rate(request):
    user = User.objects.get(id=request.session.get("user_id"))
    print(type(user.rate_set.all()))
    rate = user.rate_set.all()

    return render(request, "my_rate.html", {"rate": rate})

@login_in
def myfoot(request):
    user = User.objects.get(id=request.session.get("user_id"))#获取当前登录用户
    print(user.id)
    # print(request.session.get("username"))
    footprint = MyFootprint.objects.filter(user_id=user.id) #get 若返回对象为空则报错
    #print(type(footprint))
    #print(footprint[0].bookname)
    return render(request, "my_footprint.html",{"myfootprint":footprint})   # 字段名 BUG
    # mysite = User.objects.get(id=request.session.get("user_id"))
    # print(type(mysite.rate_set.all()))
    # rate = mysite.rate_set.all()
    # print(rate)
    # print(rate[0].mark)
    # return render(request, "mysite/my_rate.html", {"rate": rate})

@login_in
def myinfo(request):
    user = User.objects.get(id=request.session.get("user_id"))

    return render(request, "myinfo.html", {"user": user})

@login_in
def delete_rate(request, rate_id):
    rate = Rate.objects.filter(pk=rate_id)
    if not rate:
        return render(request, "my_rate.html", {"rate": rate})
    rate = rate.first()
    rate.book.rate_num -= 1
    rate.book.save()
    rate.save()
    rate.delete()
    user = User.objects.get(id=request.session.get("user_id"))
    rate = user.rate_set.all()
    return render(request, "my_rate.html", {"rate": rate})


def hot_book(request):   #用户收藏数
    page_number = request.GET.get("page", 1)
    books = Book.objects.annotate(user_collector=Count('collect')).order_by('-user_collector')[:10]
    books = books_paginator(books[:10], page_number)
    return render(request, "item.html", {"books": books, "title": "最热书籍"})


def latest_book(request):  #书籍ID号
    page_number = request.GET.get("page", 1)
    books = books_paginator(Book.objects.order_by("-id")[:10], page_number)  #降序
    return render(request, "item.html", {"books": books, "title": "最新书籍"})




def begin(request):
    if request.method == "POST":

        email = request.POST["email"]
        print(email)  #test email

        username = request.POST["username"]

        print(username)

        result = User.objects.filter(username=username)
        if result:
            if result[0].email == email:
                result[0].password = request.POST["password"]
                return HttpResponse("修改密码成功")
            else:
                return render(request, "begin.html", {"message": "注册时的邮箱不对"})
        else:
            return render(request, "begin.html", {"message": "账号不存在"})
    return render(request, "begin.html")


def kindof(request):
    tags = Tags.objects.all()
    return render(request, "kindof.html", {"tags": tags})




#解析对象列表
def deco_list(isbn_list):
    book_list=Book.objects.filter(isbn__in=isbn_list)
    return book_list

@login_in
def reco_by_item(request):
    # 基於物品推荐
    id=request.session.get("user_id")
    print("test",id)
    title="基于物品"
    page = request.GET.get("page", 1)

    books = books_paginator(deco_list(ItemBased(str(request.session.get("user_id")))), page)
    path = request.path

    return render(
        request, "item.html", {"books": books, "path": path, "title": title}
    )


@login_in
def reco_by_user(request):
    # 基於用户推荐
    id=request.session.get("user_id")
    print("test",id)
    title="基于用户"
    page = request.GET.get("page", 1)

    books = books_paginator(deco_list(UserBased(str(request.session.get("user_id")))), page)
    path = request.path

    return render(
        request, "item.html", {"books": books, "path": path, "title": title}
    )


@login_in
def cold_boot(request):
    # 冷启动
    # 基於物品推荐
    id=request.session.get("user_id")
    print("test",id)
    title="冷启动"
    page = request.GET.get("page", 1)

    books = books_paginator(deco_list(lengqidong()), page)
    path = request.path
    return render(
        request, "item.html", {"books": books, "path": path, "title": title}
    )


@login_in
def svd(request):
    # SVD
    id=request.session.get("user_id")
    print("test",id)
    title="矩阵分解"
    page = request.GET.get("page", 1)

    books = books_paginator(deco_list(SVDGet(str(request.session.get("user_id")))), page)
    path = request.path
    return render(
        request, "useritem.html", {"books": books, "path": path, "title": title}
    )




