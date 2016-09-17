from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render

from .models import Question


# Create your views here.
def index(request):

    #Taking care of the 404 error
    try:
        questions_list = Question.objects.order_by('title')
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    context = {
        'question_list': questions_list
    }

    # This is a shortcut and saves having to use the loader class
    return render(request, "problemfinder/index.html", context)

def search(request):
    #Taking care of the 404 error
    try:
        questions_list = Question.objects.order_by('title')
    except Question.DoesNotExist:
        raise Http404("Question does not exist")


    context = {
        'question_list': questions_list
    }

    # This is a shortcut and saves having to use the loader class
    return render(request, "problemfinder/search.html", context)



def search_req(request):
    if request.method == 'GET':
        search_query = request.GET.get('q',None)

