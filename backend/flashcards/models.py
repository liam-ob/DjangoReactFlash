from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class FlashcardStack(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField()
    name = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class Flashcard(models.Model):
    ANSWER_TYPE_CHOICES = [
        ('text', 'text'),
        ('image', 'image'),
    ]

    stack = models.ForeignKey(FlashcardStack, on_delete=models.CASCADE)

    question = models.TextField()
    answer_type = models.CharField(max_length=50, choices=ANSWER_TYPE_CHOICES)
    answer_img = models.ImageField(upload_to='images/', blank=True, null=True)
    answer_char = models.CharField(max_length=1000, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def get_answer(self):
        if self.answer_type == 'text':
            return self.answer_char
        elif self.answer_type == 'image':
            return self.answer_img
        else:
            raise ValueError('Invalid answer type')


class Priority(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    flashcard = models.ForeignKey(Flashcard, on_delete=models.CASCADE)
    priority = models.IntegerField(default=1)

    class Meta:
        unique_together = ('author', 'flashcard')
