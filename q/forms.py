from django import forms

from .models import Q,A, Reply

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Q
        fields = ('question', 'question_image', 'description')

    # def cleaned_data(self, *args, **kwargs):
    #     return 
    def clean(self):
        return self.cleaned_data

class AnswerForm(forms.ModelForm):
    class Meta:
        model = A
        fields = ('answer', 'solution_image')


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('reply',)

