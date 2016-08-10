from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
# from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Question(models.Model):
    title = models.CharField(max_length=250)
    question_text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    # tags = ArrayField(models.ForeignKey(Tag), blank=True)

    def add_tag(self, tag):
        self.tags.append(tag)


class Solution(models.Model):
    question = models.ForeignKey(Question)
    solution_text = models.TextField()
    # tags = ArrayField(models.ForeignKey(Tag), blank=True)

    def add_tag(self, tag):
        self.tags.append(tag)


class Tag(models.Model):
    """
    The generic tag class
    """
    name = models.TextField()
    parent = None
    children = []

    def __str__(self):
        output = ''
        if self.parent is not None:
            output += str(self.parent)
        return (output + ':' + self.name).strip(':')

    # todo: work out why pyCharm doesn't like this. prob a django thing
    def __init__(self, name, parent):
        self.name = name
        if parent is not None:
            self.parent = parent
            parent.addChild(self)

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children


# todo: implement this where appropriate (pseudo "Main" method)
# def addTag(name, parent):
#     if parent is None:
#         tags.append(Tag(name, None))
#         return
#     parentTag = None
#     for tag in tags:
#         if tag.name == parent:
#             parentTag = tag
#             break
#     if parentTag is None:
#         addTag(parent, None)
#         tags.append(Tag(name, tags[-1]))
#     else:
#         tags.append(Tag(name, parentTag))