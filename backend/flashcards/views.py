import random
from rest_framework import views, permissions, response, status, exceptions
from rest_framework.authentication import TokenAuthentication
from django.db.models import Q, Count, Case, When, IntegerField

from . import serializers
from .models import FlashcardStack, Flashcard, Priority
from .permissions import IsAuthorOrReadOnly


class FlashcardStackListAllCreateAPIView(views.APIView):
    """List all flashcard stacks or create a new one."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        if request.user.is_anonymous:
            serializer = serializers.FlashcardStackSerializer(FlashcardStack.objects.filter(public=True), many=True)
        else:
            query = FlashcardStack.objects.filter(Q(public=True) | Q(author=request.user))
            serializer = serializers.FlashcardStackSerializer(query, many=True)
        return response.Response(serializer.data)

    def post(self, request):
        print(request.data)
        serializer = serializers.FlashcardStackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FlashcardStackDetailView(views.APIView):
    """Retrieve, update or delete a flashcard stack instance."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_object(self, pk):
        try:
            stack = FlashcardStack.objects.get(pk=pk)
        except FlashcardStack.DoesNotExist:
            raise exceptions.NotFound
        if stack.author != self.request.user and not stack.public:
            raise exceptions.PermissionDenied
        return stack

    def get(self, request, pk, format=None):
        flashcard_stack = self.get_object(pk)
        serializer = serializers.FlashcardStackSerializer(flashcard_stack)
        return response.Response(serializer.data)

    def put(self, request, pk, format=None):
        flashcard_stack = self.get_object(pk)
        serializer = serializers.FlashcardStackSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        flashcard_stack = self.get_object(pk)
        flashcard_stack.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class FlashcardListAllCreateAPIView(views.APIView):
    """List all flashcards or create a new one."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    authentication_classes = [TokenAuthentication]


    def get(self, pk, request):
        serializer = serializers.FlashcardSerializer(Flashcard.objects.filter(stack__pk=pk), many=True)
        return response.Response(serializer.data)

    def post(self, pk, request):
        serializer = serializers.FlashcardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(stack=FlashcardStack.objects.get(pk=self.kwargs['pk']))


class FlashcardDetailView(views.APIView):
    """Retrieve, update or delete a flashcard instance."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]


    def get_object(self, pk):
        try:
            return Flashcard.objects.get(pk=pk)
        except Flashcard.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk, format=None):
        flashcard = self.get_object(pk)
        serializer = serializers.FlashcardSerializer(flashcard)
        return response.Response(serializer.data)

    def put(self, request, pk, format=None):
        flashcard = self.get_object(pk)
        serializer = serializers.FlashcardSerializer(flashcard, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        flashcard = self.get_object(pk)
        flashcard.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class WeightedFlashcard(views.APIView):
    """Retrieve a random flashcard based on the priority"""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk, format=None):
        flashcard_query = Flashcard.objects.filter(stack__pk=pk)
        flashcard_query = flashcard_query.annotate(
            user_priority=Case(
                When(priority__author=request.user, then='priority__priority'),
                default=1,
                output_field=IntegerField()
            )
        )
        flashcard_list = list(flashcard_query)

        # Apply weight by simply duplicating the flashcard in the list
        weighted_flashcard_list = []
        for flashcard in flashcard_list:
            weighted_flashcard_list.extend([flashcard] * flashcard.user_priority)

        # Get a random flashcard
        flashcard = random.choice(weighted_flashcard_list)
        serializer = serializers.FlashcardSerializer(flashcard)
        return response.Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = serializers.PrioritySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

