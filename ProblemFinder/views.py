from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render

from .models import Question
from .models import Search


# Create your views here.
def index(request):

    #Taking care of the 404 error
    try:
        questions_list = Question.objects.order_by('title')
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    languages = {"C++", "Java", "C#", "Python"}
    difficulty = {"Easy", "Moderate", "Hard"}

    context = {
        'question_list': questions_list,
        'languages':languages,
        'difficulty':difficulty
    }

    # This is a shortcut and saves having to use the loader class
    return render(request, "problemfinder/index.html", context)


def search(request):
    #Taking care of the 404 error
    try:
        questions_list = Question.objects.order_by('title')
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    languages = {"----", "C++", "Java", "C#", "Python"}
    difficulty = {"----", "Easy", "Moderate", "Hard"}
    query = ''
    found = None

    if ('q' in request.GET) and request.GET['q'].strip():
        query = request.GET['q']

    lan = request.GET.get('language', '----')
    difft = request.GET.get('difficulty', '----')
    newQuestionList = []
    searchResult = Search(query, questions_list)

    if(searchResult == questions_list):
        newQuestionList = searchResult
    else:
        if(isinstance(searchResult, list)):
            for result in searchResult:
                newQuestionList.append(result)

    context = {
        'question_list': newQuestionList,
        'query': query,
        'languages': languages,
        'difficulty': difficulty,
        'languagesel': lan,
        'difft':difft,
    }

    # This is a shortcut and saves having to use the loader class
    return render(request, "problemfinder/search.html", context)