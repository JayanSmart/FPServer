from django.contrib.auth import authenticate
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Question, Solution

global user_flag  # Determine if this is a staff member or not
user_flag = False
global user_value  # The username of the logged in user
user_value = ""



# Create your views here.
def index(request):
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

    # User login form functionality
    if ('username' in request.POST) and request.POST['username'].strip():
        username = request.POST['username']
        if ('password' in request.POST) and request.POST['password'].strip():
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                user_value = user
                user_flag = True

    # Create a list with all tags to help html queries
    all_tags = []
    for question in questions_list:
        for tag in question.tags.all():
            if tag not in all_tags:
                all_tags.append(tag)

    local_user = user_value

    # All elements passed to index.html
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

    # User login form
    if ('username' in request.POST) and request.POST['username'].strip():
        username = request.POST['username']
        if ('password' in request.POST) and request.POST['password'].strip():
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                user_value = user
                user_flag = True

    # Initialising search query
    query = ''

    # Getting search query from search bar
    if ('q' in request.GET) and request.GET['q'].strip():
        query = request.GET['q']

    # Getting language and difficulty dropdown box selection
    lan = request.GET.get('language', '----')
    difft = request.GET.get('difficulty', '----')

    if difft == "Difficulty" or difft == "----":
        difft = "Not Selected"
    if lan == "Language" or lan == "----":
        lan = "Not Selected"

    new_question_list = []
    # Calling the search algorithm
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
    """
    This is the main search algorithm used
    :rtype: list
    :param query: This is an array of tags and titels that the user searched for
    :param questions_list: This is a list of all the question on the DB
    :param language: The language of the desired solution
    :param difficulty: The difficulty of the problem as prescribed by the user
    :param user_flag: This is a boolean flag that tells the algorithm if the user is logged in and can see hidden problems
    :return: This will return a list of all the problems that match the search parameters
    """

    # The list which we will be returning
    list_return = []

    for question in questions_list:
        if not question.visible and not user_flag:  # Checks if user can access invisible questions
            continue
        else:
            # Title + Difficulty + Language Search
            if query.lower() in question.title.lower():  # If the search query is in the database of questions
                if language_difficulty_check(question, language, difficulty):
                    list_return.append(question)

            # Tag Search, Checks Language + Difficulty too
            if query != "":  # Only need to check tags if query is populated (optimisation)
                for tag in question.tags.all():  # Loop through all of the questions tags and look for match
                    if query in str(tag).split('.')[-1]:  # If tag matches query, check language & difficulty
                        if language_difficulty_check(question, language, difficulty):
                            list_return.append(question)

    # Remove duplicates
    final_list = []
    for i in list_return:
        if i not in final_list:
            final_list.append(i)

    return final_list


def language_difficulty_check(question, language, difficulty):
    diff_hash = {'2': 'Easy', '3': 'Moderate', '4': 'Hard'}  # Helps difficulty search
    lang_hash = {'2': 'Java', '3': 'Python', '4': 'C++'}  # Helps language search

    if language == "Not Selected":
        if difficulty == "Not Selected":  # If language and difficulty not selected
            return True
        else:
            if diff_hash.get(question.difficulty) == difficulty:  # If language not selected but difficulty selected
                return True
    elif difficulty == "Not Selected":
        for solution in question.solutions.all():  # If difficulty not selected but language selected
            if lang_hash.get(solution.language) == language:
                return True
    elif diff_hash.get(question.difficulty) == difficulty:  # If difficulty and language selected
        for solution in question.solutions.all():
            if lang_hash.get(solution.language) == language:
                return True

    return False


def get_children(search_tag, tag_list):
    """
    returns a list of all the child tags of a given tag, this method is recursive and will search for more than one
    level of children (e.g. grand-children)
    :rtype: list
    :param search_tag: This is the parent tag for which we want the children
    :param tag_list: This is the list of all tags in the DB at the time of query
    :return: A list of all the unique child tags of some particular tag (search_tag)
    """
    list_return = []

    for tag in tag_list:
        if str(tag.parent) == str(search_tag):
            list_return.append(tag)
            list_return.extend(get_children(tag, tag_list))
    return list(set(list_return))  # This will return a list of unique elements
