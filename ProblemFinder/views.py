from django.contrib.auth.forms import AuthenticationForm
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .models import Question, Solution
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
import base64

global user_flag
user_flag = False
global user_value
user_value = ""


# Create your views here.
def index(request):
    global user_flag
    global user_value

    #Populating variable with all question objects
    try:
        questions_list = Question.objects.order_by('title')
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    #Lists of all possible languages and difficulties
    languages = Solution.LANGUAGE
    difficulty = Question.DIFFICULTY

    #Used to see if a user is logged in or not
    userFlag = False;

    #Check if logout button was clicked
    if ('logout' in request.GET) and request.GET['logout'].strip():
        user_flag = False

    # User login form functionality
    if ('username' in request.POST) and request.POST['username'].strip():
        username = request.POST['username']
        if ('password' in request.POST) and request.POST['password'].strip():
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                user_value = user
                user_flag = True

    #Create a list with all tags to help html queries
    all_tags = []
    for question in questions_list:
        for tag in question.tags.all():
            if tag not in all_tags:
                all_tags.append(tag)

    local_user = user_value

    #All elements passed to index.html
    context = {
        'question_list': questions_list,
        'languages': languages,
        'difficulty': difficulty,
        'tag_list': all_tags,
        'user_flag': user_flag,
        'user_value': local_user,
    }

    # This is a shortcut and saves having to use the loader class
    return render(request, "problemfinder/index.html", context)


def search(request):
    global user_flag
    global user_value

    # Populating variable with all question objects
    try:
        questions_list = Question.objects.order_by('title')
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    # Lists of all possible languages and difficulties
    languages = Solution.LANGUAGE
    difficulty = Question.DIFFICULTY

    # Check if logout button was clicked
    if ('logout' in request.GET) and request.GET['logout'].strip():
        user_flag = False

    #User login form
    if ('username' in request.POST) and request.POST['username'].strip():
        username = request.POST['username']
        if ('password' in request.POST) and request.POST['password'].strip():
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                user_value = user
                user_flag = True

    #Initialising search query
    query = ''

    #Getting search query from search bar
    if ('q' in request.GET) and request.GET['q'].strip():
        query = request.GET['q']

    #Getting language and difficulty dropdown box selection
    lan = request.GET.get('language', '----')
    difft = request.GET.get('difficulty', '----')

    if difft == "Difficulty" or difft == "----":
        difft = "Not Selected"
    if lan == "Language" or lan == "----":
        lan = "Not Selected"


    new_question_list = []
    #Calling the search algorithm
    searchResult = search_alg(query, questions_list, lan, difft, user_flag)

    if searchResult == questions_list:
        new_question_list = searchResult
    else:
        if isinstance(searchResult, list):
            for result in searchResult:
                new_question_list.append(result)

    # Create a list with all tags to help html queries
    all_tags = []
    for question in questions_list:
        for tag in question.tags.all():
            if tag not in all_tags:
                all_tags.append(tag)

    local_user = user_value

    # All elements passed to index.html
    context = {
        'question_list': new_question_list,
        'query': query,
        'languages': languages,
        'difficulty': difficulty,
        'languagesel': lan,
        'difft': difft,
        'tag_list': all_tags,
        'user_flag': user_flag,
        'user_value': local_user,
    }

    # This is a shortcut and saves having to use the loader class
    return render(request, "problemfinder/search.html", context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'problemfinder/details.html', {'question': question})


# The Search Algorithm
def search_alg(query, questions_list, language, difficulty, user_flag):

    # The list which we will be returning
    list_return = []

    for question in questions_list:
            if not question.visible and not user_flag: #Checks if user can access invisible questions
                continue
            else:
                # Title + Difficulty + Language Search
                if query.lower() in question.title.lower():  # If the search query is in the database of questions
                   list_return.extend(language_difficulty_check(question,language,difficulty))

                # Tag Search, Checks Language + Difficulty too
                if query != "":                                  #Only need to check tags if query is populated (optimisation)
                    for tag in question.tags.all():              #Loop through all of the questions tags and look for match
                        if query in str(tag).split('.')[-1]:     #If tag match query, then check if language and difficulty match question
                            list_return.extend(language_difficulty_check(question, language, difficulty))

    #Remove duplicates
    final_list = []
    for i in list_return:
        if i not in final_list:
            final_list.append(i)

    return final_list


def language_difficulty_check(question, language, difficulty):
    diffHash = {'2': 'Easy', '3': 'Moderate', '4': 'Hard'}    #Helps difficulty search
    langHash = {'2': 'Java', '3': 'Python', '4': 'C++'}       #Helps language search
    list_return = []

    if (language == "Not Selected"):
        if (difficulty == "Not Selected"):  #If language and difficulty not selected
            list_return.append(question)
        else:
            if (diffHash.get(question.difficulty) == difficulty):  #If language not selected but difficulty selected
                list_return.append(question)
    elif (difficulty == "Not Selected"):
        for solution in question.solutions.all():                  #If difficulty not selected but language selected
            if (langHash.get(solution.language) == language):
                list_return.append(question)
    elif (diffHash.get(question.difficulty) == difficulty):        #If difficulty and language selected
        for solution in question.solutions.all():
            if (langHash.get(solution.language) == language):
                list_return.append(question)

    return list_return
