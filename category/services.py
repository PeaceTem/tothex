from sre_parse import CATEGORIES


# create services that will take care of adding CATEGORIES
# removing categories and others allied operations


# def addCategoryService(user, category):

def removeFirstUserCategory(user, profile):
    if user.myCategories.count() > 9:
        first_user_cat = user.myCategories.first()
        profile.categories.remove(first_user_cat.category)
        first_user_cat.delete()
        # user.myCategories.first().delete()