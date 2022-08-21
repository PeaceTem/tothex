
from .models import PostAd
from quiz.utils import randomChoice

def getAd(page):
    postAd = PostAd.objects.all()
    if postAd.count() > 0:
        postAd = randomChoice(postAd)

        postAd.views += 1
        if page == "detail":
            postAd.detailpageviews += 1
        elif page == "submit":
            postAd.submitpageviews += 1
        elif page == "banner":
            postAd.bannerpageviews += 1
        elif page == "correction":
            postAd.correctionpageviews += 1
        postAd.save()
        return postAd
    return None