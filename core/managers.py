from django.db import models


class ProfileQuerySet(models.QuerySet):

    def get_quizzes_taken_by_the_profile(self, profile):
        return self.get(id=profile.id).quizTaken.all()

    def get_selected_and_prefetched_data(self, user, *args, **kwargs):
        selected = None
        prefetched = None
        try:
            if not kwargs['selected'] == None:
                selected = kwargs['selected']
        except KeyError:
            pass

        try:
            prefetched = kwargs['prefetched']
        except KeyError:
            pass


        if selected and prefetched:
            
            return self.select_related(*selected).prefetch_related(*prefetched).get(user=user)
        elif selected and not prefetched:
            return self.select_related(*selected).get(user=user)
        elif prefetched and not selected:
            print(*prefetched)
            return self.prefetch_related(*prefetched).get(user=user)
        else:
            return self.get(user=user)


class ProfileManager(models.Manager):

    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def get_quizzes_taken_by_the_profile(self, profile):
        return self.get_queryset().get_quizzes_taken_by_the_profile(profile)

    def get_selected_and_prefetched_data(self, user, *args, **kwargs):
        return self.get_queryset().get_selected_and_prefetched_data(user, *args, **kwargs)
