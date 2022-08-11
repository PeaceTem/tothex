


from .models import Profile, Device
from .tasks import ReferralTask


#USERDOMAIN
#OS
#HTTP_SEC_CH_UA_PLATFORM
#HTTP_SEC_CH_UA
# HTTP_USER_AGENT

# try using get_or_create
# The cookie should only last for 7 days
def ReferralService(request, code):
    try:
        try:
            device = Device.objects.get(HTTP_USER_AGENT=request.META['HTTP_USER_AGENT'],
            HTTP_SEC_CH_UA=request.META['HTTP_SEC_CH_UA'],
            HTTP_SEC_CH_UA_PLATFORM=request.META['HTTP_SEC_CH_UA_PLATFORM'])
            return
        except:
            pass
        
        Device.objects.create(HTTP_USER_AGENT=request.META['HTTP_USER_AGENT'],
            HTTP_SEC_CH_UA=request.META['HTTP_SEC_CH_UA'],
            HTTP_SEC_CH_UA_PLATFORM=request.META['HTTP_SEC_CH_UA_PLATFORM'])
        profile = Profile.objects.get(code=code)
        profile.coins += 20
        profile.refercount += 1
        profile.save()

        # ReferralTask.delay(profile.user)
        # total = Profile.objects.all().count()
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