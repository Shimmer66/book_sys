# from django.contrib import admin
#
# from .models import *
#
# admin.site.site_header = '系统管理'
# admin.site.site_title = '系统管理'
# admin.site.index_title = '系统管理'
# # Register your models here.
# class UserAdmin(admin.ModelAdmin):
#     list_display = ("username", "password", "name",  "email")
#     search_fields = ("username", "name", "phone", "email")
#
#
# class BookAdmin(admin.ModelAdmin):
#     list_display = ("title", "author", "collector", "good")
#     search_fields = ("title", "author", "good")
#     list_filter = ("author", "good")
#
#
# class ScoreAdmin(admin.ModelAdmin):
#     list_display = ("book_sys", "num", "com", "fen")
#     search_fields = ("book_sys", "num", "com", "fen")
#
#
# class ActionAdmin(admin.ModelAdmin):
#     def show_all_join(self, obj):
#         return [a.name for a in obj.user.all()]
#
#     def num(self, obj):
#         return obj.user.count()
#
#     list_display = ("title", "num", "status")
#     search_fields = ("title", "content", "mysite")
#     list_filter = ("status",)
#
#
# class CommenAdmin(admin.ModelAdmin):
#     list_display = ("mysite", "book_sys", "good", "create_time")
#     search_fields = ("mysite", "book_sys", "good")
#     list_filter = ("mysite", "book_sys")
#
#
# class ActionCommenAdmin(admin.ModelAdmin):
#     list_display = ("mysite", "action", "create_time")
#     search_fields = ("mysite", "action")
#     list_filter = ("mysite", "action")
#
#
# class LiuyanAdmin(admin.ModelAdmin):
#     list_display = ("mysite", "create_time")
#     search_fields = ("mysite",)
#     list_filter = ("mysite",)
#
#
# class NumAdmin(admin.ModelAdmin):
#     list_display = ("users", "books", "comments", "actions", "message_boards")
#
#     def get_queryset(self, request):
#         users = User.objects.all().count()
#         books = Book.objects.all().count()
#         comments = Comment.objects.all().count()
#         actions = Action.objects.all().count()
#         message_boards = Messageboard.objects.all().count()
#         if Num.objects.all().count() == 0:
#             Num.objects.create(users=users, books=books, comments=comments, actions=actions,
#                                message_boards=message_boards, )
#         else:
#             for num in Num.objects.all():
#                 num.users = users
#                 num.books = books
#                 num.comments = comments
#                 num.actions = actions
#                 num.message_boards = message_boards
#                 num.save()
#         return super().get_queryset(request)
#
#
# admin.site.register(Tags)
# admin.site.register(User, UserAdmin)
# admin.site.register(Book, BookAdmin)
# # admin.site.register(Score, ScoreAdmin)
# admin.site.register(Action, ActionAdmin)
# admin.site.register(Comment, CommenAdmin)
# admin.site.register(Actioncomment, ActionCommenAdmin)
# admin.site.register(Messageboard, LiuyanAdmin)
# admin.site.register(Num, NumAdmin)
