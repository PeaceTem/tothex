from django import forms

from .models import FeedBack, Profile, Link




class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)


    
class ProfileCreationForm(forms.ModelForm):
    date_of_birth = forms.DateTimeField(input_formats=['%d/%m/%Y'])
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "middle_name", "email", "bio", "gender", "date_of_birth", "preferred_age", "state_of_residence", "state_of_origin", "nationality", "language1", "language2", )
        # exclude = ['user', 'date_updated', 'coins', 'link', 'streak', 'code', 'referrer', 'views', 'picture', 'refercount', 'slug', 'relevance', 'categories', 'quizTaken', 'trueOrFalseQuestionsMissed', 'fourChoicesQuestionsMissed', 'trueOrFalseQuestionsTaken', 'fourChoicesQuestionsTaken', 'quizAvgScore', 'questionAvgScore', 'quizAttempts', 'questionAttempts', 'likes', 'quizzes', 'favoriteQuizzes']


class NewLinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = '__all__'
        exclude = ('profile', 'clicks', 'date_updated')





class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ('title', 'feedback')


        