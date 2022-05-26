from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import PostAd
from .forms import NewPostAdForm
from random import shuffle
from quiz.utils import randomChoice
# Create your views here.

def PostAdView(request,nextpage):
    postAd = PostAd.objects.all()
    postAd = randomChoice(postAd)
    postAd.views += 1
    postAd.bannerpageviews += 1
    postAd.save()
    

    context={
        'postAd': postAd,
        'nextpage': nextpage,
    }

    return render(request, 'ads/postAd.html', context)




def PostAdClick(request, post_id, location):
    # link_id = request.GET.get('link_id')
    user = request.user
    print(location)
    postAd = PostAd.objects.prefetch_related("clickers").get(id=post_id)

    postAd.clicks += 1
    postAd.clickers.add(user)
    if location == "detail":
        postAd.detailpageclicks += 1
    elif location == "submit":
        postAd.submitpageclicks += 1
    elif location == "banner":
        postAd.bannerpageclicks += 1
    elif location == "correction":
        postAd.correctionpageclicks += 1
    postAd.save()
    print(postAd.clicks)

    return HttpResponse('clicked')