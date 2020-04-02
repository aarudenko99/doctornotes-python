from django_mysql.models import JSONField, Model
from django.db import models
from django.contrib.auth.models import User

from utils.current_request import get_current_request


class Category(Model):
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Tag(Model):
    title = models.CharField(max_length=100)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Note(Model):
    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'
    STATUS_UNPUBLISHED = 'status_unpublished'

    STATUSES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_UNPUBLISHED, 'Unpublished')
    )

    author = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    status = models.CharField(
        choices=STATUSES, default=STATUS_PUBLISHED, max_length=30)
    json = JSONField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.author:
            request = get_current_request()
            if request:
                self.author = request.user
        return super(Note, self).save(force_insert=False, force_update=False, using=None,
                                      update_fields=None)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.title

    def is_favorite(self, user_id):
        return self.favorites.filter(user__id=user_id).exists()


class DraftNote(Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    checkboxes = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        if self.subject:
            return f'{self.subject} - {self.note.title}'
        return f'{self.note.title}'


class FavoriteNotes(Model):
    note = models.ForeignKey(
        Note, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorites')
    created = models.DateTimeField(auto_now_add=True)
