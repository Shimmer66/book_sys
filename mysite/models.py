# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `#managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

# 如果不指定，字段名默认为app_name， 而表明默认为app名+类名： [app_name]_info.
#
# verbose_name指定在admin管理界面中显示中文；verbose_name表示单数形式的显示，
# verbose_name_plural表示复数形式的显示；中文的单数和复数一般不作区别。
from django.db import models
class RatingsExplicit(models.Model):
    userid = models.CharField(db_column='userID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    isbn = models.CharField(db_column='ISBN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    bookrating = models.CharField(db_column='bookRating', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'RatingsExplicit'


class RatingsImplicit(models.Model):
    userid = models.CharField(db_column='userID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    isbn = models.CharField(db_column='ISBN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    bookrating = models.CharField(db_column='bookRating', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'RatingsImplicit'

class User(models.Model):
    username = models.CharField(unique=True, max_length=32)
    password = models.CharField(max_length=32)
    phone = models.CharField(max_length=32)
    name = models.CharField(unique=True, max_length=32)
    email = models.CharField(max_length=254)

    class Meta:
        #managed = False
        db_table = 'user_user'

class Action(models.Model):
    user = models.ManyToManyField(User, verbose_name="参加用户", blank=True)
    # new = models.ManyToManyField(
    #     User, verbose_name="审核用户", related_name="newuser", blank=True
    # )
    one = models.ImageField(upload_to="media", verbose_name="第一")
    two = models.ImageField(upload_to="media", verbose_name="第二", null=True)
    three = models.ImageField(upload_to="media", verbose_name="第三", null=True)
    title = models.CharField(verbose_name="活动标题", max_length=64)
    content = models.TextField(verbose_name="活动内容")
    status = models.BooleanField(verbose_name="状态")

    class Meta:
        verbose_name = "活动"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title



class ActionUser(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE,verbose_name="活动")
    user = models.ForeignKey('User', on_delete=models.CASCADE,verbose_name="用户")

    class Meta:
        #managed = False
        db_table = 'ActionUser'
        unique_together = (('action', 'user'),)


class Actioncomment(models.Model):
    comment = models.TextField(verbose_name="评论")
    create_time = models.DateTimeField(verbose_name="创建时间")
    action = models.ForeignKey(Action, on_delete=models.CASCADE,verbose_name="活动")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        #managed = False
        db_table = 'user_actioncomment'


class Boardcomment(models.Model):
    content = models.TextField()
    create_time = models.DateTimeField()
    message_board = models.ForeignKey('Messageboard', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        #managed = False
        db_table = 'user_boardcomment'

class Tags(models.Model):
    name = models.CharField(max_length=32,verbose_name="标签")

    class Meta:
        #managed = False
        db_table = 'user_tags'


class Book(models.Model):
    tags = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        verbose_name="标签",
        related_name="tags",
        blank=True,
        null=True,
    )
    collect = models.ManyToManyField(User, verbose_name="收藏者", blank=True)
    collector = models.IntegerField(default=0,verbose_name="收藏人数")
    title = models.CharField(max_length=255,null=False,verbose_name="标题")
    author = models.CharField(max_length=255,null=False,verbose_name="作者")
    intro = models.TextField( null=True,verbose_name="内容简介")
    num = models.IntegerField(default=0,null=True,verbose_name="浏览数")
    imageurlm = models.CharField(db_column='imageUrlM', max_length=255, blank=False,null=True,verbose_name="图片地址")  # Field name made lowercase.
    good = models.CharField(max_length=32,verbose_name="点赞数")
    rate_num = models.IntegerField( default=0,verbose_name="评分人数")
    isbn = models.CharField(db_column='ISBN', max_length=255, blank=True, null=True,verbose_name="ISBN")  # Field name made lowercase.
    yearofpublication = models.CharField(db_column='yearOfPublication', max_length=255, blank=False,verbose_name="出版日期")  # Field name made lowercase.
    publisher = models.CharField(max_length=255, blank=True,verbose_name="出版社")

    class Meta:
        #managed = False
        db_table = 'user_book'

    def __str__(self):
        return self.title
class Messageboard(models.Model):
    title = models.CharField(max_length=255,verbose_name="标题")
    content = models.TextField(verbose_name="评论内容")
    look_num = models.IntegerField(default=1,verbose_name="浏览量")
    like_num = models.IntegerField(default=0,verbose_name="点赞数")
    feebback_num = models.IntegerField(default=0,verbose_name="回复人数")
    collect_num = models.IntegerField(default=0,verbose_name="收藏数")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    user = models.ForeignKey('User', on_delete=models.CASCADE,verbose_name="用户")

    class Meta:
        #managed = False
        db_table = 'user_Messageboard'

class Collectboard(models.Model):
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    is_collect = models.IntegerField(default=False,verbose_name="收藏状态")
    is_like = models.IntegerField(default=False,verbose_name="点赞")
    message_board = models.ForeignKey(Messageboard, on_delete=models.CASCADE)
    user = models.ForeignKey(User,  on_delete=models.CASCADE,)

    class Meta:
        #managed = False
        db_table = 'user_Collectboard'


class Comment(models.Model):
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    good = models.IntegerField(default=0,verbose_name="点赞")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        #managed = False
        db_table = 'user_comment'


class Num(models.Model):
    users = models.IntegerField(default=0)
    books = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    rates = models.IntegerField(default=0)
    actions = models.IntegerField(default=0)
    message_boards = models.IntegerField(default=0)

    class Meta:
        #managed = False
        db_table = 'user_num'


class Rate(models.Model):
    mark = models.FloatField(verbose_name="评分")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True, )
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'user_rate'



class UsersExpRatings(models.Model):
    userid = models.CharField(db_column='userID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255, blank=True, null=True)  # Field name made lowercase.
    age = models.CharField(db_column='Age', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'users_exp_ratings'


class UsersImpRatings(models.Model):
    userid = models.CharField(db_column='userID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255, blank=True, null=True)  # Field name made lowercase.
    age = models.CharField(db_column='Age', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        #managed = False
        db_table = 'users_imp_ratings'
class MyFootprint(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    username= models.CharField(db_column='username', max_length=255, blank=True, null=True)  # Field name made lowercase.
    bookname= models.CharField(db_column='bookname', max_length=255, blank=True, null=True)  # Field name made lowercase.
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True, )
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True)
    url= models.CharField(db_column='url', max_length=255, blank=True, null=True)  # Field name made lowercase.
    class Meta:
        #managed = False
        db_table = 'user_footprint'
