from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import FileExtensionValidator, MaxLengthValidator
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
    stack = models.ForeignKey(FlashcardStack, on_delete=models.CASCADE)

    question = models.TextField()
    answer_img = models.ImageField(upload_to='media/images', blank=True, null=True,
                                    validators=[FileExtensionValidator(['png', 'jpg', 'jpeg']), MaxLengthValidator(2*1024*1024)])
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
