from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import ProblemFinder


# Create your models here.
class Tag(models.Model):
    """
    The generic tag class
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


class Solution(models.Model):
    """
    This is a generic Solution Class
    """
    # Enum for possible difficulty
    LANGUAGE_CHOICES = (
        ('1', '----'),
        ('2', 'Java'),
        ('3', 'Python'),
        ('4', 'C++')
    )

    LANGUAGE = {"----", "Java", "Python", "C++"}

    description = models.TextField()
    solution_text = models.TextField(blank=True)
    solution_URL = models.URLField(blank=True)
    solution_PDF = models.FileField(upload_to='uploads/', blank=True)
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


class Question(models.Model):
    """
    This is a generic Question Class
    """

    # Enums for difficulty to show stuff
    DIFFICULTY_CHOICES = (
        ('1', '----'),
        ('2', 'Easy'),
        ('3', 'Moderate'),
        ('4', 'Hard')
    )

    DIFFICULTY = {"----", "Easy", "Moderate", "Hard"}

    title = models.CharField(max_length=250)
    question_text = models.TextField(blank=True)
    question_URL = models.URLField(blank=True)
    question_PDF = models.FileField(upload_to='./ProblemFinder/pdf/', blank=True)
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


# The Search Algorithm (in progress)
def search_alg(query, questions_list, language, difficulty):
    diffHash = {'2':'Easy', '3':'Moderate','4':'Hard'}
    langHash = {'2': 'Java', '3': 'Python', '4': 'C++'}
    list_return = []  # The list which we will be returning

    for question in questions_list:
        for solution in question.solutions.all():
            print(solution)
        print(question.solutions.all())

        # Title + Difficulty Search
        if query.lower() in question.title.lower():  # If the search query is in the database of questions
            if(language == "Not Selected"):
                if(difficulty == "Not Selected"):
                    list_return.append(question)  # Add to results list
                else:
                    if (diffHash.get(question.difficulty) == difficulty):
                        list_return.append(question)  # Add to results list

            elif(difficulty == "Not Selected"):
                for solution in question.solutions.all():
                    if (langHash.get(solution.language) == language):
                        list_return.append(question)  # Add to results list

            elif(diffHash.get(question.difficulty) == difficulty):
                for solution in question.solutions.all():
                    if(langHash.get(solution.language) == language):
                        list_return.append(question)  # Add to results list

        # Tag Search

        print(question.tags)  # WHY IS THIS PRINTING ProblemFinder.Tags.None??????????
        for tag in question.tags.all():  # Loop through all of the questions tags and look for match
            if str(tag).split('.')[-1] == query:
                list_return.append(question)  # If match then append to list

    return list_return


# Search for a matching Title, Tag and Difficulty
def search_general(query, questions_list, difficulty):
    diffs = {'2': 'Java', '3': 'Python', '4': 'C++'}
    matched_list = []
    # Check Difficulty (fastest)
    for quest in questions_list:
        if diffs[quest.difficulty] == difficulty:
            # Check Tag (moderate)
            if query in quest.tags.all():
                # Check Title (slowest)
                if query in quest.titel.split('.'):
                    matched_list.append(quest)

    return matched_list
