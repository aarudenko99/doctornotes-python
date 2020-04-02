from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse

from .models import Category, Macro, Type, Tag
from .forms import NoteForm


def is_valid_queryparam(param):
    return param != '' and param is not None


@login_required
def create_note(request):

    if request.method == 'POST':
        form = NoteForm(request.POST)

        if form.is_valid():
            form.save()
        form = NoteForm()
    else:
        form = NoteForm()

    qs = Macro.objects.all()
    categories = Category.objects.all()
    types = Type.objects.all()
    tags = Tag.objects.all()
    title = request.GET.get('title')
    titles = Macro.objects.values_list('Title', flat=True)
    abbreviation = request.GET.get('macro')
    macros = Macro.objects.values_list('Abbreviation', flat=True)
    my_type = request.GET.get('type')
    tag = request.GET.get('tag')
    category = request.GET.get('category')

    if is_valid_queryparam(category) and category != 'Chooise...':
        qs = qs.filter(Category__title=category)

    if is_valid_queryparam(my_type) and my_type != 'Chooise...':
        qs = qs.filter(Type__title=my_type)

    if is_valid_queryparam(tag) and tag != 'Chooise...':
        qs = qs.filter(Tags__title=tag)

    if is_valid_queryparam(title) and title != 'Chooise...':
        qs = qs.filter(Title=title)

    if is_valid_queryparam(abbreviation) and abbreviation != 'Chooise...':
        qs = qs.filter(Abbreviation=abbreviation)

    macro = Macro.objects.all()
    macros_selialized = serializers.serialize(
                        'json',
                        macro,
                        indent=2,
                        use_natural_foreign_keys=True,
                        use_natural_primary_keys=True,
                        )
    macro_json = JsonResponse(macros_selialized, safe=False)
    print(macros_selialized)
    context = {
        'queryset': qs,
        'macros': macros,
        'categories': categories,
        'tags': tags,
        'types': types,
        'titles': titles,
        'macro_json': macros_selialized,
        'form': form
    }

    return render(request, 'macros/note_macro.html', context)




