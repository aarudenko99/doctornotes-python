from django_mysql.models import JSONField, Model
from django.db import models

from django.contrib.auth.models import User

from utils.current_request import get_current_request

class TitleFieldManager(models.Manager):
    def get_by_natural_key(self, title):
        return self.get(title=title)


class Category(Model):
    title = models.CharField(max_length=100)

    objects = TitleFieldManager()

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        unique_together = [['title']]

    def natural_key(self):
        return self.title

    def __str__(self):
        return self.title


class Tag(Model):
    title = models.CharField(max_length=100)

    objects = TitleFieldManager()

    class Meta:
        ordering = ('-id',)
        unique_together = [['title']]

    def natural_key(self):
        return self.title

    def __str__(self):
        return self.title


class Type(Model):
    title = models.CharField(max_length=100)

    objects = TitleFieldManager()

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Type'
        verbose_name_plural = 'Types'
        unique_together = [['title']]

    def natural_key(self):
        return self.title

    def __str__(self):
        return self.title


class Macro(Model):
    Type = models.ForeignKey(
        Type,
        null=True,
        blank=True,
        on_delete=models.SET_NULL)
    Tags = models.ManyToManyField(Tag, blank=True)
    Category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL)
    Abbreviation = models.CharField(max_length=100, unique=True)
    Title = models.CharField(max_length=100, verbose_name='Title')
    Content = models.TextField(max_length=10000)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.Title


class Note(Model):
    title = models.TextField(max_length=100000)