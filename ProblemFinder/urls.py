from django.conf.urls import url
from django.views.generic import ListView

from . import views

from ProblemFinder.models import Question

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^search$', views.search, name='search')
    url(r'^search$', ListView.as_view(queryset=Question.objects.all(), template_name="problemfinder/search.html")) #Sending question objects to search.html
]