from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


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
        if self.parent is not None:
            output += str(self.parent)
        return (output + ':' + self.name).strip(':')

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
    description = models.TextField()
    solution_text = models.TextField(blank=True)
    solution_URL = models.URLField(blank=True)
    solution_PDF = models.FileField(upload_to='uploads/', blank=True)
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


class Question(models.Model):
    """
    This is a generic Question Class
    """
    title = models.CharField(max_length=250)
    question_text = models.TextField(blank=True)
    question_URL = models.URLField(blank=True)
    question_PDF = models.FileField(upload_to='uploads/', blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)
    solutions = models.ManyToManyField(Solution)

    def __str__(self):
        return self.title

    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)

    name = models.CharField(max_length=512)

    def __unicode__(self):
        return self.name




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

#The Search Algorithm (in progress)
def search(difficulty, language, tagList):
    for i in Question:
        for j in Question.tags:
            if j == difficulty:
                if j == language:
                    for k in tagList:
                        if j == k:
                            return i

#Initialising search variables from search.html
def populateSearch():
    return


