from django.conf.urls import url
from django.views.generic import ListView

from ProblemFinder.models import Question
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search$', views.search, name='search'),
    url(r'^search$', ListView.as_view(queryset=Question.objects.all(), template_name="problemfinder/search.html")),  # Sending question objects to search.html
    url(r'^search/(?P<question_id>[0-9]+)/$', views.detail, name='details'),
    url(r'^login/$', views.UserFormView.as_view(), name='login'),
]
