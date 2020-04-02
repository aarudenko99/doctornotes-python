import json
import openpyxl
import random
import string
from django.contrib import admin, messages
from django import forms
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import path
from django.utils.text import slugify
from django.utils.translation import ugettext as _
from django_mysql.models import JSONField
from jsoneditor.forms import JSONEditor
from .models import Note, Category, Tag, DraftNote



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class JsonImportForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}), label=_('File to import')
    )


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'category', 'tags_list', 'title', 'slug', 'created', 'description')
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ('slug', 'title', 'category__title', 'description',)

    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }
    change_list_template = 'notes/notes_changelist.html'

    def tags_list(self, obj):
        tags = [t.title for t in obj.tags.all()]
        return ' '.join(tags) if tags else '-'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-json/', self.import_json),
            path('import-excel/', self.import_excel),
        ]
        return my_urls + urls

    def import_excel(self, request):
        form = JsonImportForm()
        if request.POST:
            form = JsonImportForm(request.POST, request.FILES)
            if form.is_valid():
                message = "Your json file(s) has been imported"
                files = request.FILES.getlist('file')
                for f in files:
                    wb = openpyxl.load_workbook(f)
                    worksheet = wb["Sheet1"]
                    i = 0
                    json_obj = ''
                    tags = None
                    for row in worksheet.iter_rows():
                        i += 1
                        if i == 1:
                            continue
                        j = 0
                        for cell in row:
                            if j == 0:
                                category = cell.value
                                j += 1
                                continue
                            if j == 1:
                                tags = cell.value
                                j += 1
                                continue
                            if j == 2:
                                title = cell.value
                                j += 1
                                continue
                            if j == 3:
                                description = cell.value
                                j += 1
                                continue
                            if j == 4:
                                slug = cell.value
                                j += 1
                                continue
                            if j == 5:
                                json_text = cell.value
                                if json_text == None:
                                    continue
                                try:
                                    json_obj = json.loads(json_text)
                                except json.decoder.JSONDecodeError as e:
                                    json_obj = ''
                                    pass
                        try:
                            cats = Category.objects.filter(title=category)
                            category_id = None
                            for cat in cats:
                                category_id = cat.id

                            def randomString(stringLength=10):
                                letters = string.ascii_lowercase
                                return ''.join(random.choice(letters) for i in range(stringLength))

                            if title == None:
                                title = randomString(10)
                            if slug == None:
                                slug = randomString(10)

                            createdNote = Note.objects.create(title=title, slug=slug, json=json_obj, category_id=category_id,  description=description)
                            if tags != None:

                                tagNames = tags.split(' ')
                                for tagName in tagNames:
                                    currentTags = Tag.objects.filter(title=tagName)
                                    # print(currentTags[0])
                                    if len(currentTags) > 0:
                                        temp = currentTags[0]
                                    else:
                                        temp = Tag(title=tagName)
                                        temp.save()

                                    createdNote.tags.add(temp)

                        except IntegrityError:
                            pass

                self.message_user(request, message)
                return redirect("..")
        payload = {"form": form, 'title': 'Upload Excel File'}
        return render(
            request, "notes/upload_form.html", payload
        )

    def import_json(self, request):
        form = JsonImportForm()
        if request.POST:
            form = JsonImportForm(request.POST, request.FILES)
            if form.is_valid():
                message = "Your json file(s) has been imported"
                files = request.FILES.getlist('file')
                for f in files:
                    title = f.name.replace('.json', '').replace('_', ' ').title()
                    slug = slugify(title)
                    json_text = (f.file.read()
                                 .decode('utf-8'))
                    try:
                        json_obj = json.loads(json_text)
                    except json.decoder.JSONDecodeError as e:
                        messages.error(request, f'{f.name} - {e}')

                    try:
                        Note.objects.create(title=title, slug=slug, json=json_obj)
                    except IntegrityError:
                        pass
                self.message_user(request, message)
                return redirect("..")
        payload = {"form": form, 'title': 'Upload JSON File'}
        return render(
            request, "notes/upload_form.html", payload
        )


@admin.register(DraftNote)
class DraftNoteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'note',
        'subject',
        'message',
        'created',
        'checkboxes',
    )
    list_filter = ('note', 'created')
