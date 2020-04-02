from django.urls import path
from . import views


urlpatterns = [
    path('', views.notes, name='notes'),
    path('notes/<category_id>/', views.notes, name='notes_category'),
    path('templates/delete/<draft_id>/', views.draft_note_delete, name='draft_note_delete'),
    path('templates/<slug>/', views.note, name='note'),
    path('templates/<slug>/<draft_id>/', views.note, name='note_draft'),

    # favorites
    path('favorite_add/<note_id>/', views.favorite_add, name='favorite_add'),
    path('favorite_delete/<note_id>/', views.favorite_delete, name='favorite_delete'),

    path('send_recommendation/', views.send_recommendation, name='send_recommendation'),
]
