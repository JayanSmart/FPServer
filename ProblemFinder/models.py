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

    def __str__(self):
        return self.name


class Solution(models.Model):
    """
    The Generic Solution Class
    """
    # Enums for Languages
    LANGUAGE_CHOICES = (
        ('1', '----'),
        ('2', 'Java'),
        ('3', 'Python'),
        ('4', 'C++')
    )

    # This is in the code twice because Django is pedantic and we need to force order...
    LANGUAGE = ("----", "Java", "Python", "C++")

    description = models.TextField(blank=True)
    solution_URL = models.URLField(blank=True)
    solution_PDF = models.FileField(blank=True)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        output = self.description + " : "
        for tag in self.tags.all():
            if tag.name in ["Java", "Python", "C#", "C++"]:
                output += tag.name
                break
        return output


class Question(models.Model):
    """
    The Generic Question Class
    """

    # Enums for difficulty
    DIFFICULTY_CHOICES = (
        ('1', '----'),
        ('2', 'Easy'),
        ('3', 'Moderate'),
        ('4', 'Hard')
    )

    DIFFICULTY = ("----", "Easy", "Moderate", "Hard")

    title = models.CharField(max_length=250)
    question_text = models.TextField(blank=True)
    question_URL = models.URLField(blank=True)
    question_PDF = models.FileField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)
    tags = models.ManyToManyField(Tag)
    solutions = models.ManyToManyField(Solution, blank=True)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title
