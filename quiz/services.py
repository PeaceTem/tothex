from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



"""
Add all the services like referral and the recommendation algorithms
create a service for getting numbers too.
"""

"""
Sentence will be self.descrition

"""
def stringCleaningService(sentence: str):
    
    if sentence is not None:
        try:
            string = sentence
            length = len(string)
            for i in range(length):
                if (string[i] == "<"):
                    for n in range(i,length):
                        if string[n] == ">":
                            raise ValidationError(_("Remove both '<' and '>'"))
                
                if (string[i] == "<") and (string[i+1] == "/"):
                    raise ValidationError(_("Remove the '</' from your description"))

                if (string[i] == "(") and (string[i+1] == "s") and (string[i+2] == "u") and (string[i+3] == "b") and (string[i+4] == ")"):
                    string2 = str.replace(string, "(sub)", "<sub>")
                    string = string2
                elif (string[i] == "(") and (string[i+1] == "/") and (string[i+2] == "s") and (string[i+3] == "u") and (string[i+4] == "b") and (string[i+5] == ")"):
                    string2 = str.replace(string, "(/sub)", "</sub>")
                    string = string2
                elif (string[i] == "(") and (string[i+1] == "s") and (string[i+2] == "u") and (string[i+3] == "p") and (string[i+4] == ")"):
                    string2 = str.replace(string, "(sup)", "<sup>")
                    string = string2
                elif (string[i] == "(") and (string[i+1] == "/") and (string[i+2] == "s") and (string[i+3] == "u") and (string[i+4] == "p") and (string[i+5] == ")"):
                    string2 = str.replace(string, "(/sup)", "</sup>")
                    string = string2
            sentence = string
            return sentence

        except:
            raise ValidationError(_('An error occurred!'))
    


def reverseStringCleaningService(sentence: str):
    if sentence is not None:
        string = sentence
        length = len(string)
        for i in range(length):
             
            if (string[i] == "<") and (string[i+1] == "s") and (string[i+2] == "u") and (string[i+3] == "b") and (string[i+4] == ">"):
                string2 = str.replace(string, "<sub>", "(sub)")
                string = string2
            elif (string[i] == "<") and (string[i+1] == "/") and (string[i+2] == "s") and (string[i+3] == "u") and (string[i+4] == "b") and (string[i+5] == ">"):
                string2 = str.replace(string, "</sub>", "(/sub)")
                string = string2
            elif (string[i] == "<") and (string[i+1] == "s") and (string[i+2] == "u") and (string[i+3] == "p") and (string[i+4] == ">"):
                string2 = str.replace(string, "<sup>", "(sup)")
                string = string2
            elif (string[i] == "<") and (string[i+1] == "/") and (string[i+2] == "s") and (string[i+3] == "u") and (string[i+4] == "p") and (string[i+5] == ">"):
                string2 = str.replace(string, "</sup>", "(/sup)")
                string = string2

        sentence = string
        return sentence






def ScoreRange(value: int):
    if value == 0:
        return 50
    else:
        return 100 - value





def generateCoins(score, average_score, length, *args, **kwargs):
    result = (2 - (score/100)) * (average_score/100) * length
    return result





def get_random_quiz(user):
    profile = Profile.objects.prefetch_related("categories").get(user=user)
    categories = profile.categories.all()
    quizzes = Quiz.objects.filter(categories__in=categories, questionLength__gte=10, solution_quality__gt=3, average_score__gte=50).distinct()[:100]
    quiz = None
    if not quizzes.count() > 0:
        quizzes = Quiz.objects.filter(categories__in=categories, questionLength__gte=10, solution_quality__gt=0).distinct()[:100]

    
    if not quizzes.count() > 0:
        quizzes = Quiz.objects.filter(categories__in=categories, questionLength__gte=10)[:100]

    if quizzes.count() > 0:
        quiz = randomChoice(quizzes)
        return quiz

    return None