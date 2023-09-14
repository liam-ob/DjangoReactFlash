from django.urls import path

from . import views

app_name = 'flashcards'
urlpatterns = [
    path('flashcardstacks/listcreate/', views.FlashcardStackListAllCreateAPIView.as_view(), name='flashcardstacks-listcreate'),
    path('flashcardstacks/<int:pk>/', views.FlashcardStackDetailView.as_view(), name='flashcardstack-detail'),
    path('flashcard/weightedflashcard/', views.WeightedFlashcard.as_view(), name='weightedflashcard'),
]
