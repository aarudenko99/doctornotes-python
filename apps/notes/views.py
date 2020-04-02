import json

from django.contrib.auth.decorators import login_required
from django.db.models import BooleanField, Case, Value, When
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse

from utils.simple_message import send_simple_message

from .forms import SaveDraftForm, SendEmailForm, SendRecommendationForm
from .models import Category, DraftNote, FavoriteNotes, Note


@login_required
def notes(request, category_id=None):
    context = {}
    categories = Category.objects.all()
    notes_qs = (
        Note.objects
            .filter(status=Note.STATUS_PUBLISHED)
            .annotate(
                is_favorite=Case(
                    When(favorites__user__id=request.user.id, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
        .values('slug', 'title', 'is_favorite')
    )

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        notes_qs = notes_qs.filter(category=category)
        context['category_id'] = int(category_id)

    notes_list = list(notes_qs)
    notes_draft = DraftNote.objects.filter(user=request.user)
    context.update({
        'notes': json.dumps(notes_list),
        'notes_draft': notes_draft,
        'categories': categories,
    })

    return render(
        request,
        template_name='notes/notes.html',
        context=context
    )


@login_required
def note(request, slug, draft_id=None):
    note_instance = get_object_or_404(Note, slug=slug)
    context = {
        'note': note_instance,
        'is_favorite': note_instance.is_favorite(request.user.id),
        'checkboxes': [],
    }
    form = SaveDraftForm()
    form_recommendation = SendRecommendationForm(initial={
        'note_id': note_instance.id,
        'subject': note_instance.title
    })

    if draft_id:
        draft = get_object_or_404(DraftNote, id=draft_id, note=note_instance)
        form = SaveDraftForm(initial={
            'subject': draft.subject,
            'message': draft.message,
        })
        context['checkboxes'] = []
        context['draft_id'] = draft_id
        if draft.checkboxes:
            context['checkboxes'] = draft.checkboxes.split(',')

    if request.method == 'POST' and 'send_email' in request.POST:
        form = SendEmailForm(request.POST)
        if form.is_valid():
            send_simple_message(
                form.cleaned_data.get('subject'),
                form.cleaned_data.get('message'),
                'sohailvaghari@gmail.com',
                [form.cleaned_data.get('send_to')],
            )
            context['email_success'] = 'Email has been sent'

    if request.method == 'POST':
        form = SaveDraftForm(request.POST)
        if form.is_valid():
            context['checkboxes'] = form.cleaned_data \
                .get('checkboxes').split(',')
            draft_data = dict(note=note_instance,
                              subject=form.cleaned_data.get('subject'),
                              message=form.cleaned_data.get('message'),
                              checkboxes=form.cleaned_data.get('checkboxes'),
                              )
            if 'save_draft' in request.POST:
                draft = DraftNote.objects.create(**draft_data, user=request.user)
                draft_id = draft.id
                context['draft_success'] = 'Draft has been saved'
            elif 'update_draft' in request.POST:
                if draft_id:
                    DraftNote.objects.filter(id=draft_id).update(**draft_data)
                    context['draft_success'] = 'Draft has been updated'

    context['form'] = form
    context['form_recommendation'] = form_recommendation

    if context.get('draft_success'):
        return HttpResponseRedirect(reverse('note_draft', args=[slug, draft_id]))

    return render(
        request,
        template_name='notes/note.html',
        context=context,
    )


@login_required
def draft_note_delete(request, draft_id):
    draftnote = get_object_or_404(DraftNote, id=draft_id, user=request.user)
    draftnote.delete()
    return HttpResponseRedirect(reverse('notes'))


@login_required
def favorite_add(request, note_id):
    fav_note = get_object_or_404(Note, id=note_id)
    FavoriteNotes.objects.get_or_create(note=fav_note, user=request.user)
    return HttpResponseRedirect(reverse('note', args=[fav_note.slug]))


@login_required
def favorite_delete(request, note_id):
    fav_note = get_object_or_404(
        FavoriteNotes, note__id=note_id, user=request.user)
    fav_note.delete()
    return HttpResponseRedirect(reverse('note', args=[fav_note.note.slug]))


@login_required
def send_recommendation(request):
    if not request.method == 'POST':
        return JsonResponse(data={'error': 'method not allowed'})

    context = {}
    form = SendRecommendationForm(request.POST)
    if form.is_valid():
        note_link = form.cleaned_data.get('note_id')
        message = form.cleaned_data.get('message')
        message += f'\n\nNote link: {note_link}'
        send_simple_message(
            form.cleaned_data.get('subject'),
            message,
            'system@docktornotes.com',
            ['sohailvaghari@gmail.com'],
        )
        context['email_success'] = 'Email has been sent'
        return JsonResponse(data={'success': 'form has been send'})

    content = render_to_string(
        'notes/send_recommendation.html', {'form': form}, request=request)
    return JsonResponse(data={'error': True, 'content': content})
