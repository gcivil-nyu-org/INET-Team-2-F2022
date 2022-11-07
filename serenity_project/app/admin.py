from django.contrib import admin
from .models import ScoreTable, ForumPost, Comment

# Register your models here.

admin.site.register(ScoreTable)
admin.site.register(ForumPost)
admin.site.register(Comment)
