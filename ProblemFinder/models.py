# Finding Problems
# Course: CSC3003S
# Date: 23 September 2016

# Imports
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


# Tag
class Tag(models.Model):
    """
    The generic tag class
    tags are binded to all question and solution objects
    """
    name = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True)
    children = []

    def __str__(self):
        output = ''
        return (self.name).strip(':')

    def add_tag(self, name, parent):
        new_tag(name, parent)

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children

# Solution
class Solution(models.Model):
    """
    This is a generic Solution Class
    """

    LANGUAGE_CHOICES = ("----", "Java", "Python", "C++")

    description = models.TextField()
    solution_text = models.TextField(blank=True)
    solution_URL = models.URLField(blank=True)
    solution_PDF = models.FileField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        output = self.description + " : "
        for tag in self.tags.all():
            if tag.name in ["Java", "Python", "C#", "C++"]:
                output += tag.name
                break
        return output

    def add_tag(self, tag):
        self.tags.append(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)

    def get_tags(self):
        return self.tags.all()

# Question
class Question(models.Model):
    """
    This is a generic Question Class
    """

    # Enums for difficulty to show stuff

    DIFFICULTY_CHOICES = ("----", "Easy", "Moderate", "Hard")

    title = models.CharField(max_length=250)
    question_text = models.TextField(blank=True)
    question_URL = models.URLField(blank=True)
    question_PDF = models.FileField()
    created_date = models.DateTimeField(default=timezone.now)
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)
    tags = models.ManyToManyField(Tag)
    solutions = models.ManyToManyField(Solution)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)

    # Create a dynamic upload url.
    # Thinking of trying to host online?
    # Google Drive/Dropbox account that we access from the code. I'm sure there is an API for it.
    def get_upload_to(self):
        return True #TODO: Finish this method


# Misc Functions

# This is for the Tag model
def new_tag(name, parent):
    if parent is None:
        Tag.objects.create(name, None)
        return
    parent_tag = None
    for tag in Tag.objects.all():
        if tag.name == parent:
            parent_tag = Tag.objects.get(parent)
            break
    if parent_tag is None:
        new_tag(parent, None)
        new_tag(name, parent)
    else:
        made_tag = Tag.objects.create(name, parent_tag)
        parent_tag.add_child(made_tag)


# Search Algorithm (in progress)
#

def search_alg(query, questions_list, language, difficulty):
    list_return = []         # The list which we will be returning

    for question in questions_list:
        if(question.visible == False):        # Checks if question has been marked as 'invisible'
            break
        else:
            # Title + Difficulty + Language Search
            if query.lower() in question.title.lower():       # If the search query is in the database of questions
                # Call language_difficulty_check() method
               list_return.extend(language_difficulty_check(question,language,difficulty))

            # Tag Search, Checks language + difficulty too
            if query != "":                                  # Only need to check tags if query is populated (optimisation)
                for tag in question.tags.all():              # Loop through all of the questions tags and look for match
                    if query in str(tag).split('.')[-1]:     # If tag match query, then check if language and difficulty match question
                        # Call language_difficulty_check() method
                        list_return.extend(language_difficulty_check(question, language, difficulty))

    # Remove duplicates
    final_list = []
    for i in list_return:
        if i not in final_list:
            final_list.append(i)

    return final_list

def language_difficulty_check(question, language, difficulty):
    diffHash = {'2': 'Easy', '3': 'Moderate', '4': 'Hard'}    # Helps difficulty search
    langHash = {'2': 'Java', '3': 'Python', '4': 'C++'}       # Helps language search
    list_return = []

    if (language == "Not Selected"):
        if (difficulty == "Not Selected"):  # If language and difficulty not selected
            list_return.append(question)
        else:
            if (diffHash.get(question.difficulty) == difficulty):  # If language not selected but difficulty selected
                list_return.append(question)
    elif (difficulty == "Not Selected"):
        for solution in question.solutions.all():                  # If difficulty not selected but language selected
            if (langHash.get(solution.language) == language):
                list_return.append(question)
    elif (diffHash.get(question.difficulty) == difficulty):        # If difficulty and language selected
        for solution in question.solutions.all():
            if (langHash.get(solution.language) == language):
                list_return.append(question)

    return list_return