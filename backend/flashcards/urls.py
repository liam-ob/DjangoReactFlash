from django.urls import path

from . import views

app_name = 'flashcards'
urlpatterns = [
    path('flashcardstacks/listcreate/', views.FlashcardStackListAllCreateAPIView.as_view(), name='flashcardstacks-listcreate'),
    path('flashcardstacks/<int:pk>/', views.FlashcardStackDetailView.as_view(), name='flashcardstack-detail'),
    path('flashcards/listcreate/<int:pk>/', views.FlashcardListAllCreateAPIView.as_view(), name='flashcards-listcreate'),
    path('flashcards/detail/<int:pk>/', views.FlashcardDetailView.as_view(), name='flashcard-detail'),
    path('flashcards/weightedflashcard/<int:pk>/', views.WeightedFlashcard.as_view(), name='weightedflashcard'),
]
