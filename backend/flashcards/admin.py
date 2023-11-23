from django.contrib import admin
from .models import FlashcardStack, Flashcard, Priority
# Register your models here.
admin.site.register(FlashcardStack)
admin.site.register(Flashcard)
admin.site.register(Priority)