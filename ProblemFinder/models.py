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

    def addTag(self, name, parent):
        new_tag(name, parent)

    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children


class Question(models.Model):
    title = models.CharField(max_length=250)
    question_text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField(Tag)

    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)


class Solution(models.Model):
    question = models.ForeignKey(Question)
    solution_text = models.TextField()
    tags = models.ManyToManyField(Tag)

    def add_tag(self, tag):
        self.tags.append(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)


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