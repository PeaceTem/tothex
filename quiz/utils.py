import random

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=fetch_resources)
     if not pdf.err:
          return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None

def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))

    return path





def sortKey(e):
    return e[0]


def sortQuiz(e):
     return e.relevance



def randomCoin():
     value = (1,2,3)
     goal = random.choices(value, weights=[10,20,1], k=1)
     return goal[0]

def randomChoice(value):
     goal = random.choices(value, k=1)
     return goal[0]

def adsRandom():
     value = ('ads', 'noAds')
     goal = random.choices(value, weights=[1,30], k=1)
     return goal[0]

def quizRandomCoin():
     value=(5,7,10)
     goal = random.choices(value, weights=[100,10,1], k=1)
     return goal[0]



