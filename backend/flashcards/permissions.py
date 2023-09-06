from rest_framework import permissions
from .models import FlashcardStack, Flashcard


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow authors of an object to edit it."""

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, FlashcardStack):
            return obj.author == request.user
        elif isinstance(obj, Flashcard):
            return obj.stack.author == request.user
        else:
            raise ValueError('The object is not a FlashcardStack or Flashcard')
