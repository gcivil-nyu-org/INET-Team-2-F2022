from django.contrib import admin
from .models import ScoreTable, Forum, Discussion

# Register your models here.

admin.site.register(ScoreTable)
admin.site.register(Forum)
admin.site.register(Discussion)
