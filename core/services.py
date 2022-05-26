


from .models import Profile, Device
from .tasks import ReferralTask




# try using get_or_create
def ReferralService(device, code):
    try:
        device = device
        try:
            device = Device.objects.get(name=device)
            return
        except:
            pass

        Device.objects.create(name=device)
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
