
from django import forms
from .models import FourChoicesQuestion, TrueOrFalseQuestion
from category.models import Category
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
class NewFourChoicesQuestionForm(forms.ModelForm):

    class Meta:
        model = FourChoicesQuestion
        fields = '__all__'
        exclude = ('user', 'quiz', 'form', 'index', 'date_created', 'standalone', 'categories', 'attempts', 'avgScore',  'solution_quality', 'solution_validators', 'answer1NumberOfTimesTaken', 'answer2NumberOfTimesTaken', 'answer3NumberOfTimesTaken', 'answer4NumberOfTimesTaken', 'relevance',)



class NewTrueOrFalseQuestionForm(forms.ModelForm):

    class Meta:
        model = TrueOrFalseQuestion
        fields = '__all__'
        exclude = ('user', 'quiz', 'form', 'index', 'answer1', 'answer2', 'standalone', 'categories', 'solution_validators' , 'date_created', 'categories', 'attempts', 'avgScore',  'solution_quality', 'solution_validators', 'answer1NumberOfTimesTaken', 'answer2NumberOfTimesTaken', 'relevance',)

    def clean(self):
        a1 = self.cleaned_data.get('age_from')
        a2 = self.cleaned_data.get('age_to')
        if a1 is not None and a2 is not None and a1 > a2:
            raise ValidationError(_('minimum age should be less than or equal too maximum age'))

        self.cleaned_data    




class QuizGeneratorForm(forms.Form):
    duration_in_minutes = forms.IntegerField()
    number_of_questions = forms.IntegerField()
    
    