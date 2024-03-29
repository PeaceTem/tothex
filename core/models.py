
from django.db import models
from django.contrib.auth.models import User


from quiz.models import Quiz
from category.models import Category
from question.models import TrueOrFalseQuestion, FourChoicesQuestion
from datetime import date, datetime, time, timedelta
from django.core.exceptions import ValidationError
# from .utils import generate_ref_code
# from quiz.idpk import finalConvert
from django.utils.text import slugify
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import pytz

from ckeditor.fields import RichTextField
from .managers import ProfileManager

from .utils import getSimplifiedNumber

# Create your models here.


class Profile(models.Model):

    SEX =(
        ('male', 'male'),
        ('female', 'female'),
    )
    user = models.OneToOneField(User,null=True, blank=True, on_delete=models.CASCADE, related_name='profile')
    picture = models.ImageField(upload_to='images/profile/', null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Last Name"))
    middle_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Middle Name"))
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name=_("Email"))
    bio = models.TextField(max_length=1000, null=True, blank=True, verbose_name=_("Biography"))
    gender = models.CharField(max_length=10, choices=SEX, null=True, blank=True, verbose_name=_("Gender"))
    date_of_birth = models.DateField(null=True, blank=True, verbose_name=_("Date Of Birth"))
    preferred_age = models.PositiveSmallIntegerField(default=15, help_text=_("This is the age that will be used to generate quizzes and questions to you!"))
    state_of_residence = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("state Of Residence"))
    state_of_origin = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("State Of Origin"))
    nationality = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Nationlity"))
    language1 = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("First Language"))
    language2 = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Second Language"))

    coins = models.DecimalField(default=20.0, decimal_places=2, max_digits=200)
    total_coins = models.FloatField(default=0)
    date_updated = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=32, null=True, blank=True)
    refercount = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    # This will be taken out from this place
    categories = models.ManyToManyField(Category, blank=True, related_name='profileCategories')
    quizTaken = models.ManyToManyField(Quiz, blank=True, related_name='profileQuizTaken')
    quizWareHouse = models.ManyToManyField(Quiz, blank=True, related_name='profileQuizWareHouse')

    trueOrFalseQuestionsTaken = models.ManyToManyField(TrueOrFalseQuestion, blank=True, related_name='trueOrFalseQuestionsTaken')
    fourChoicesQuestionsTaken = models.ManyToManyField(FourChoicesQuestion, blank=True, related_name='fourChoicesQuestionsTaken')
    
    trueOrFalseQuestionsMissed = models.ManyToManyField(TrueOrFalseQuestion, blank=True, related_name='trueOrFalseQuestionsMissed')
    fourChoicesQuestionsMissed = models.ManyToManyField(FourChoicesQuestion, blank=True, related_name='fourChoicesQuestionsMissed')
    
    trueOrFalseQuestionsWareHouse = models.ManyToManyField(TrueOrFalseQuestion, blank=True, related_name='trueOrFalseQuestionsWareHouse')
    fourChoicesQuestionsWareHouse = models.ManyToManyField(FourChoicesQuestion, blank=True, related_name='fourChoicesQuestionsWareHouse')

    quizAvgScore = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    questionAvgScore = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    quizAttempts = models.IntegerField(default=0)
    questionAttempts = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    quizzes = models.IntegerField(default=0)
    favoriteQuizzes = models.ManyToManyField(Quiz, blank=True, related_name='favoriteQuizzes')
    favoriteUser = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='favoriteUser')
    last_question_date = models.DateTimeField(null=True)
    recommended_quizzes = models.ManyToManyField(Quiz, blank=True, related_name='recommended_quizzes_profiles')
    recommended_four_choices_questions = models.ManyToManyField(FourChoicesQuestion, blank=True, related_name='recommended_four_choices_questions_profiles')
    recommended_true_or_false_questions = models.ManyToManyField(TrueOrFalseQuestion, blank=True, related_name='recommended_true_or_false_questions_profiles')
    following_four_choices_questions = models.ManyToManyField(FourChoicesQuestion, blank=True, related_name='following_four_choices_questions_profiles')
    following_true_or_false_questions = models.ManyToManyField(TrueOrFalseQuestion, blank=True, related_name='following_true_or_false_questions_profiles')
    



    objects = ProfileManager()
    """
    
    Add the clean method to allow only users with age 3 and above to use the platform
    """

    @property
    def get_user_age(self):
        return self.preferred_age


    @property
    def get_number_of_quiz_created(self):
        num = self.quizzes
        return getSimplifiedNumber(num)






    @property
    def get_number_of_likes(self):
        num = self.likes
        return getSimplifiedNumber(num)



    @property
    def get_number_of_quizzes_attempted(self):
        num = self.quizAttempts
        return getSimplifiedNumber(num)





    @property
    def get_number_of_questions_attempted(self):
        num = self.questionAttempts
        return getSimplifiedNumber(num)


    def __str__(self):
        return f"{self.user}"


 
class Follower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='follower')
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    following = models.ManyToManyField(User, blank=True, related_name='following')


    @property
    def get_number_of_followers(self):
        num = self.followers.all().count()
        return getSimplifiedNumber(num)




    @property
    def get_number_of_following(self):
        num = self.following.all().count()
        return getSimplifiedNumber(num)
    

    def __str__(self):
        return f"{self.user}"
# create the streak in the app views and validate it thereafter


class Streak(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=False)
    # change this to default
    length = models.PositiveIntegerField(default=0)
    question = models.PositiveIntegerField(default=0)
    freeze = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.profile}"

# alert users whenever they earn a streak

    def validateStreak(self,value, *args, **kwargs):
        for i in range(value):

            self.question += 1

            if self.question == 20 and self.active == False:
                self.length += 1
                self.active = True
                self.profile.coins += 20
                self.profile.save()

            elif self.question == 50 and self.active == True:
                self.profile.coins += 60
                self.profile.save()
            
            elif self.question == 100 and self.active == True:
                self.profile.coins += 120
                self.profile.save()
            
        super().save(*args, **kwargs)

        # add streak freeze product in the wallet
        # users can pay us dollars to buy anything



        # return self.length




# add description
class Link(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='link')
    name = models.CharField(max_length=20, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    description = models.TextField(max_length=200,blank=True, null=True)
    clicks = models.PositiveIntegerField(default=0)
    date_updated = models.DateTimeField(null=True, blank=True)




    @property
    def get_number_of_clicks(self):
        num = self.clicks
        if num < 1000:
            return num
        elif num < 1000000:
            num = num / 1000
            num = round(num, 1)
            return f"{num}k"
        elif num < 1000000000:
            num = num / 1000000
            num = round(num, 1)
            return f"{num}M"
        elif num < 1000000000000:
            num = num / 1000000000
            num = round(num, 1)
            return f"{num}B"
        return num



    def __str__(self):
        return f"{self.profile}"





"""
Change this place and use def clean instead
"""


"""
Delete the instances of this model every month.
"""
class Device(models.Model):
    HTTP_USER_AGENT = models.CharField(max_length=1000)
    HTTP_SEC_CH_UA = models.CharField(max_length=1000)
    HTTP_SEC_CH_UA_PLATFORM = models.CharField(max_length=1000)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.HTTP_SEC_CH_UA}"


class FeedBack(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    feedback = RichTextField(verbose_name=_("Feedback"))
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"



