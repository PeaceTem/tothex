from django.db import models


class FourChoicesQuestionQuerySet(models.QuerySet):
    def get_smaller_than(self, size):
        return self.filter(attempts__lt=size)

    def get_user_questions(self, user):
        return self.filter(user=user)


class FourChoicesQuestionManager(models.Manager):

    def get_queryset(self):
        return FourChoicesQuestionQuerySet(self.model, using=self._db)

    def get_user_quizzes(self, user):
        return self.get_queryset().get_user_questions(user)

    def get_smaller_than(self, size):
        return self.get_queryset().get_smaller_than(size)





        
class TrueOrFalseQuestionQuerySet(models.QuerySet):
    def get_smaller_than(self, size):
        return self.filter(attempts__lt=size)

    def get_user_questions(self, user):
        return self.filter(user=user)


class TrueOrFalseQuestionManager(models.Manager):

    def get_queryset(self):
        return TrueOrFalseQuestionQuerySet(self.model, using=self._db)

    def get_user_quizzes(self, user):
        return self.get_queryset().get_user_questions(user)

    def get_smaller_than(self, size):
        return self.get_queryset().get_smaller_than(size)