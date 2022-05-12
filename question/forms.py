
from django import forms
from .models import FourChoicesQuestion, TrueOrFalseQuestion
from category.models import Category

class NewFourChoicesQuestionForm(forms.ModelForm):

    class Meta:
        model = FourChoicesQuestion
        fields = '__all__'
        exclude = ('user', 'form', 'index', 'date_created', 'standalone', 'categories', 'attempts', 'avgScore',  'solution_quality', 'solution_validators', 'answer1NumberOfTimesTaken', 'answer2NumberOfTimesTaken', 'answer3NumberOfTimesTaken', 'answer4NumberOfTimesTaken', 'relevance',)



class NewTrueOrFalseQuestionForm(forms.ModelForm):

    class Meta:
        model = TrueOrFalseQuestion
        fields = '__all__'
        exclude = ('user', 'form', 'index', 'answer1', 'answer2', 'standalone', 'categories', 'solution_validators' , 'date_created', 'categories', 'attempts', 'avgScore',  'solution_quality', 'solution_validators', 'answer1NumberOfTimesTaken', 'answer2NumberOfTimesTaken', 'relevance',)




class QuizGeneratorForm(forms.Form):
    duration_in_minutes = forms.IntegerField()
    number_of_questions = forms.IntegerField()
    
    