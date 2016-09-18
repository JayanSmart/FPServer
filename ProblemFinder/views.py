from django.http import Http404
from django.shortcuts import render

from .models import Question, Solution
from .models import search_alg


# Create your views here.
def index(request):

    #Taking care of the 404 error
    try:
        questions_list = Question.objects.order_by('title')
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    languages = Solution.LANGUAGE
    difficulty = Question.DIFFICULTY
    context = {
        'question_list': questions_list,
        'languages': languages,
        'difficulty': difficulty
    }

    # This is a shortcut and saves having to use the loader class
    return render(request, "problemfinder/index.html", context)


def search(request):
    #Taking care of the 404 error
    try:
        questions_list = Question.objects.filter(visible=True).order_by('title')
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    languages = Solution.LANGUAGE
    difficulty = Question.DIFFICULTY
    query = ''

    if ('q' in request.GET) and request.GET['q'].strip():
        query = request.GET['q']

    lan = request.GET.get('language', '----')
    difft = request.GET.get('difficulty', '----')

    if difft == "Difficulty" or difft == "----":
        difft = "Not Selected"


    new_question_list = []
    searchResult = search_alg(query, questions_list, lan, difft)

    if searchResult == questions_list:
        new_question_list = searchResult
    else:
        if isinstance(searchResult, list):
            for result in searchResult:
                new_question_list.append(result)


    # soln_lang = []
    # for quest in new_question_list:
    #     for soln in quest.solutions.all():
    #         soln_lang.append(soln.language)  #Adding question solution tags
    #
    # new_soln_lang = []
    # for i in soln_lang:
    #     if(i == "2"):
    #         new_soln_lang.append("Java")
    #     elif(i == "3"):
    #         new_soln_lang.append("Python")
    #     elif(i == "4"):
    #         new_soln_lang.append("C++")
    # print(new_soln_lang)


    context = {
        'question_list': new_question_list,
        'query': query,
        'languages': languages,
        'difficulty': difficulty,
        'languagesel': lan,
        'difft':difft,
    }

    # This is a shortcut and saves having to use the loader class
    return render(request, "problemfinder/search.html", context)