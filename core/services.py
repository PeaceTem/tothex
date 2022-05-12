


from .models import Profile
from .tasks import ReferralTask





def ReferralService(code):
    try:
        print("Starting the referral service!")
        profile = Profile.objects.select_related('user').get(code=code)
        profile.coins += 20
        profile.refercount += 1
        profile.save()

        ReferralTask.delay(profile.user)
        total = Profile.objects.all().count()
        print(total)
        print("Ending the referral service!")
    except:
        pass    

    return
