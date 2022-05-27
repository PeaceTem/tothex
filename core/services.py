


from .models import Profile, Device
from .tasks import ReferralTask


#USERDOMAIN
#OS
#HTTP_SEC_CH_UA_PLATFORM
#HTTP_SEC_CH_UA

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


def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split('.')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip