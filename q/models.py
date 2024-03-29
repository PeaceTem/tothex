from django.db import models
from core.models import Profile
from category.models import Category
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.


class Q(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    question = models.CharField(max_length=200, verbose_name=_("Question"), unique=True)
    question_image = models.ImageField(blank=True, null=True, upload_to='images/qxa/question/', verbose_name=_("Photo"))
    description = models.TextField(max_length=1000, verbose_name=_("Description"))
    categories = models.ManyToManyField(Category, blank=True, related_name='qs')
    views = models.PositiveIntegerField(default=0)
    upvoters = models.ManyToManyField(Profile, blank=True, related_name='upvoted_questions')
    downvoters= models.ManyToManyField(Profile, blank=True, related_name='downvoted_questions')
    slug = models.SlugField(unique=True, null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.question}"

    class Meta:
        ordering=['-date','-date_updated']



    def save(self, *args, **kwargs):
        self.slug = slugify(self.question) + '-' + str(self.id)
        return super().save(*args, **kwargs)



# leave deleted if the question is inactive or deleted
class SavedQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Q, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"{self.question}"


class A(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='answers')
    answer = models.TextField(max_length=10000, verbose_name=_("Answer"))
    solution_image = models.ImageField(upload_to='images/qxa/answer/', verbose_name=_("Photo"), blank=True, null=True)
    upvoters = models.ManyToManyField(Profile, blank=True, related_name='upvoted_answers')
    downvoters = models.ManyToManyField(Profile, blank=True, related_name='downvoted_answers')
    question = models.ForeignKey(Q, on_delete=models.CASCADE, related_name='answers')    
    date = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.answer}"


# add replies later
class Reply(models.Model):
	answer = models.ForeignKey(A, on_delete=models.CASCADE, related_name='replies')
	profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='replies')
	reply = models.CharField(max_length=1000)
	date = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)


	def __str__(self):
		return f"{self.reply}"




