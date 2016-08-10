from django.contrib import admin
from .models import Question, Tag, Solution


# Register your models here.

admin.site.register(Question)
admin.site.register(Solution)
admin.site.register(Tag)