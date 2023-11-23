import random

from rest_framework import views, permissions, response, status, exceptions
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.db.models import Q, Count, Case, When, IntegerField, Prefetch
from django.utils import timezone

from . import serializers
from .models import FlashcardStack, Flashcard, Priority
from .permissions import IsAuthorOrReadOnly


class FlashcardStackListAllCreateAPIView(views.APIView):
    """List all flashcard stacks or create a new one."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        if request.user.is_anonymous:
            serializer = serializers.FlashcardStackSerializer(FlashcardStack.objects.filter(public=True), many=True)
        else:
            query = FlashcardStack.objects.filter(Q(public=True) | Q(author=request.user))
            serializer = serializers.FlashcardStackSerializer(query, many=True)
        return response.Response(serializer.data)

    def post(self, request):
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
    authentication_classes = [TokenAuthentication, SessionAuthentication]

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
        request.data['date_modified'] = timezone.now()
        serializer = serializers.FlashcardStackSerializer(flashcard_stack, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(serializer.instance, request.data)
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        flashcard_stack = self.get_object(pk)
        flashcard_stack.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class FlashcardListAllCreateAPIView(views.APIView):
    """List all flashcards or create a new one."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request, pk):
        stack = FlashcardStack.objects.get(pk=pk)
        if stack.author != request.user and not stack.public:
            raise exceptions.PermissionDenied
        
        flashcards_with_priority = Flashcard.objects.filter(stack=stack).annotate(
            user_priority=Priority.objects.filter(author=request.user, flashcard__stack=stack).values('priority')
        )
        serializer = serializers.FlashcardSerializerWithPriority(flashcards_with_priority, many=True)
        return response.Response(serializer.data)

    def post(self, request, pk):
        if not request.data.get('stack_id', None):
            raise exceptions.ValidationError({'stack_id': 'This field is required.'})
        if request.user != FlashcardStack.objects.get(pk=request.data['stack_id']).author:
            raise exceptions.PermissionDenied
        serializer = serializers.FlashcardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(stack=FlashcardStack.objects.get(pk=self.kwargs['pk']))


class FlashcardDetailView(views.APIView):
    """Retrieve, update or delete a flashcard instance."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_object(self, pk):
        try:
            obj = Flashcard.objects.get(pk=pk)
            if obj.stack.author != self.request.user and not obj.stack.public:
                raise exceptions.PermissionDenied
            return obj
        except Flashcard.DoesNotExist:
            raise exceptions.NotFound

    def get(self, request, pk, format=None):
        flashcard = self.get_object(pk)
        serializer = serializers.FlashcardSerializer(flashcard)
        return response.Response(serializer.data)

    def put(self, request, pk, format=None):
        flashcard = self.get_object(pk)
        if request.user != flashcard.stack.author:
            raise exceptions.PermissionDenied
        request_data = request.data.copy()
        request_data['date_modified'] = timezone.now()
        serializer = serializers.FlashcardSerializer(flashcard, data=request_data)
        if serializer.is_valid():
            serializer.update(serializer.instance, request_data)
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        flashcard = self.get_object(pk)
        if request.user != flashcard.stack.author:
            raise exceptions.PermissionDenied
        flashcard.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class WeightedFlashcard(views.APIView):
    """Retrieve a random flashcard based on the priority"""
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    # pk here is the stack pk (different then the post)
    def get(self, request, pk, format=None):
        # Create a priority for the user if there isnt one already
        if not Priority.objects.filter(author=request.user, flashcard__stack__pk=pk).exists():
            Priority.objects.bulk_create(
                [Priority(author=request.user, flashcard=flashcard) for flashcard in
                 Flashcard.objects.filter(stack__pk=pk)]
            )
        flashcard_query = Flashcard.objects.filter(
            stack__pk=pk, priority__author=request.user
        ).annotate(
            user_priority=Case(
                When(priority__author=request.user, then='priority__priority'),
                default=1,
                output_field=IntegerField(),
            ),
            priority_id=Case(
                When(priority__author=request.user, then='priority__id'),
                default=None,
                output_field=IntegerField(),
            )
        )
        flashcard_list = list(flashcard_query)
        if not flashcard_list:
            raise exceptions.NotFound('No flashcards found in this stack.')

        # Apply weight by simply duplicating the flashcard in the list
        weighted_flashcard_list = []
        for flashcard in flashcard_list:
            weighted_flashcard_list.extend([flashcard] * flashcard.user_priority)

        # Get a random flashcard
        flashcard = random.choice(weighted_flashcard_list)
        serializer = serializers.FlashcardSerializerWithPriority(flashcard)
        return response.Response(serializer.data)

    # pk here is the flashcard pk (different from get)
    def post(self, request, pk, format=None):
        priority = Priority.objects.get(author=request.user, flashcard__pk=pk)
        serializer = serializers.PrioritySerializer(priority, data=request.data)
        if serializer.is_valid():
            serializer.update(serializer.instance, request.data)
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
