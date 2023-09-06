from rest_framework import serializers
from django.contrib.auth.models import User

from flashcards.models import FlashcardStack


class UserSerializer(serializers.ModelSerializer):
    flashcards_stacks = serializers.PrimaryKeyRelatedField(many=True, queryset=FlashcardStack.objects.all())

    class Meta:
        model = User
        fields = ("id", "username", "email")


class GetUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
