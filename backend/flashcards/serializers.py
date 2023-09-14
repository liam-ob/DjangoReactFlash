from rest_framework import serializers

from core.serializers import UserSerializer
from .models import FlashcardStack, Flashcard, Priority


class FlashcardStackSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    author = UserSerializer(read_only=True, required=False)
    name = serializers.CharField(max_length=100)
    public = serializers.BooleanField()
    difficulty = serializers.CharField(max_length=20)
    date_created = serializers.DateTimeField(read_only=True, required=False)
    date_modified = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        return FlashcardStack.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.public = validated_data.get('public', instance.public)
        instance.category = validated_data.get('category', instance.category)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)
        instance.date_modified = validated_data.get('date_modified', instance.date_modified)
        instance.save()
        return instance


class FlashcardSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    stack = FlashcardStackSerializer(read_only=True)
    question = serializers.CharField(max_length=1000)
    answer_type = serializers.CharField(max_length=1000)
    answer_img = serializers.ImageField(required=False)
    answer_char = serializers.CharField(max_length=1000, required=False)
    date_created = serializers.DateTimeField(read_only=True)
    date_modified = serializers.DateTimeField()
    priority = serializers.IntegerField()

    def create(self, validated_data):
        return Flashcard.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.stack = validated_data.get('stack', instance.stack)
        instance.question = validated_data.get('question', instance.question)
        instance.answer_type = validated_data.get('answer_type', instance.answer_type)
        instance.answer_img = validated_data.get('answer_img', instance.answer_img)
        instance.answer_char = validated_data.get('answer_char', instance.answer_char)
        instance.date_modified = validated_data.get('date_modified', instance.date_modified)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.save()
        return instance


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ['id', 'priority']
