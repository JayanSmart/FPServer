from django.contrib.auth import authenticate
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Question, Solution, Tag

global user_flag  # Determine if this is a staff member or not
user_flag = False
global user_value  # The username of the logged in user
user_value = ""


# Create your views here.
def index(request):
    """
    This is the logic for the home page
    :param request: HTTP request
    :return: render --> HTTP response
    """
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
    """
    This is the logic for the search page
    :param request: This is an HTTP request
    :return: render --> HTTP Response
    """
    global user_flag
    global user_value

    # Populating variable with all question objects
    try:
        questions_list = Question.objects.order_by('title')
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    # populate a var with all available tags
    try:
        tag_list = Tag.objects.all()
    except Tag.DoesNotExist:
        raise Http404("Tag does not exist")

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
    querystr = ""

    # Getting search query from search bar
    if ('query' in request.GET) and request.GET['query'].strip():
        querystr = request.GET['query']
    query = querystr.split(",")
    query = query[:-1]

    # Getting language and difficulty dropdown box selection
    lang = request.GET.get('language', '----')
    difft = request.GET.get('difficulty', '----')

    if difft == "Difficulty" or difft == "----":
        difft = "Not Selected"
    if lang == "Language" or lang == "----":
        lang = "Not Selected"

    new_question_list = []
    # Calling the search algorithm
    search_result = search_alg(query, questions_list, tag_list, lang, difft)

    if search_result == questions_list:
        new_question_list = search_result
    else:
        if isinstance(search_result, list):  # This is for if there are no search matches.
            for result in search_result:
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
        'languagesel': lang,
        'difft': difft,
        'tag_list': all_tags,
        'user_flag': user_flag,
        'user_value': local_user,
        'query_list': []
    }

    # This is a shortcut and saves having to use the loader class
    return render(request, "problemfinder/search.html", context)


def detail(request, question_id):
    """
    This is the logic for the page the shows a specific questions solutions
    :param request: HTTP request
    :param question_id: The id of the question about which details are requested
    :return: render --> HTTP response
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'problemfinder/details.html', {'question': question})


def get_tag(tag_name, tag_list):
    """
    Returns the tag object when given the tag name
    :rtype: Tag
    :param tag_name: the name of the tag you want to get
    :param tag_list: list of all tags in DB at time of query
    :return: Tag object with matching name
    """
    for i in range(len(tag_list)):
        if tag_name == str(tag_list[i]):
            return tag_list[i]


# The Search Algorithm
def search_alg(query, questions_list, tag_list, language, difficulty):
    """
    This is the main search algorithm used

    :rtype: list
    :param query: This is an array of tags and titles that the user searched for
    :param questions_list: This is a list of all the question on the DB
    :param tag_list: This is a list of all the tags in the db at the time of search
    :param language: The language of the desired solution
    :param difficulty: The difficulty of the problem as prescribed by the user
    :return: This will return a list of all the problems that match the search parameters
    """
    global user_flag
    list_return = []  # The list which we will be returning
    query_tags = []
    query_titels = []

    if not query:
        query_tags = tag_list.all()
    else:
        for item in query:
            if item in map(str, tag_list):
                query_tags.append(get_tag(item, tag_list))
                query_tags.extend(get_children(item, tag_list))
            else:
                query_titels.append(item)
    for question in questions_list:
        assert isinstance(question, Question)
        if question.visible or user_flag:
            # Tag search
            question_tags = list(question.tags.all())
            for soln in question.solutions.all():
                for tag in soln.tags.all():
                    question_tags.append(tag)
            for quest_tag in question_tags:
                if quest_tag in query_tags:
                    print("here")
                    if language_difficulty_check(question, language, difficulty):
                        list_return.append(question)
                        continue
            # Title search
            for title in query_titels:
                assert isinstance(title, str)
                if title.lower() == question.title.lower() and language_difficulty_check(question, language, difficulty):
                    list_return.append(question)

    return list(set(list_return))  # This removes duplicates


def language_difficulty_check(question, language, difficulty):
    """

    :rtype: bool
    :param question: the question that is tested
    :param language: the language to look for
    :param difficulty: the difficulty to look for
    :return: True if the question matches the desired parameters, else False
    """
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
