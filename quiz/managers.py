from django.db import models
from core.managers import ProfileQuerySet

class QuizQuerySet(models.QuerySet):
    def get_smaller_than(self, size):
        return self.filter(attempts__lt=size)

    def get_user_quizzes(self, user):
        return self.filter(user=user)

    def get_random_quiz(self, user):
        profile = ProfileQuerySet.prefetch_related("categories").get(user=user)
        categories = profile.categories.all()
        quizzes = self.filter(categories__in=categories, questionLength__gte=10, solution_quality__gt=3, average_score__gte=50).distinct()[:100]
        quiz = None
        if not quizzes.count() > 0:
            quizzes = self.filter(categories__in=categories, questionLength__gte=10, solution_quality__gt=0).distinct()[:100]

        
        if not quizzes.count() > 0:
            quizzes = self.filter(categories__in=categories, questionLength__gte=10)[:100]

        if quizzes.count() > 0:
            quiz = randomChoice(quizzes)
            return quiz

        return None


class QuizManager(models.Manager):

    def get_queryset(self):
        return QuizQuerySet(self.model, using=self._db)

    def get_user_quizzes(self, user):
        return self.get_queryset().get_user_quizzes(user)

    def get_smaller_than(self, size):
        return self.get_queryset().get_smaller_than(size)

    
    def get_random_quiz(self, user):
        return self.get_queryset().get_random_quiz(user)