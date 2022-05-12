from django.db import models


class QuizQuerySet(models.QuerySet):
    def get_smaller_than(self, size):
        return self.filter(attempts__lt=size)

    def get_user_quizzes(self, user):
        return self.filter(user=user)


class QuizManager(models.Manager):

    def get_queryset(self):
        return QuizQuerySet(self.model, using=self._db)

    def get_user_quizzes(self, user):
        return self.get_queryset().get_user_quizzes(user)

    def get_smaller_than(self, size):
        return self.get_queryset().get_smaller_than(size)