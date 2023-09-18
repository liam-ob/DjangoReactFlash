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
        instance.name = validated_data.get('name', instance.name)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)
        instance.date_modified = validated_data.get('date_modified', instance.date_modified)
        instance.save()
        return instance


class FlashcardSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    stack_id = serializers.IntegerField()
    question = serializers.CharField(max_length=1000)
    answer_img = serializers.ImageField(required=False)
    answer_char = serializers.CharField(max_length=1000, required=False)
    date_created = serializers.DateTimeField(read_only=True)
    date_modified = serializers.DateTimeField(required=False)

    def is_valid(self, *, raise_exception=False):
        if not self.initial_data.get('answer_char') and not self.initial_data.get('answer_img'):
            raise serializers.ValidationError({'answer_char': 'This field is required.'})

        try:
            FlashcardStack.objects.get(id=self.initial_data.get('stack_id'))
        except FlashcardStack.DoesNotExist:
            raise serializers.ValidationError({'stack_id': 'please use a valid id'})

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        stack_id = validated_data.pop('stack_id')
        validated_data['stack'] = FlashcardStack.objects.get(id=stack_id)
        return Flashcard.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Get the stack via id to make serializing easier
        instance.stack = FlashcardStack.objects.get(id=validated_data.get('stack', instance.stack_id))

        instance.question = validated_data.get('question', instance.question)
        instance.answer_img = validated_data.get('answer_img', instance.answer_img)
        instance.answer_char = validated_data.get('answer_char', instance.answer_char)
        instance.date_modified = validated_data.get('date_modified', instance.date_modified)
        instance.save()
        return instance


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ['id', 'priority']
