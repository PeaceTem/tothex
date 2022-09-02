from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from .models import Category
# Create your views here.
from django.views import View
from django.forms import model_to_dict
from django.http import HttpResponse
from .serializers import CategorySerializer
from rest_framework import generics
from django.views.generic.base import TemplateView
from rest_framework.response import Response



class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # def get(self, request):
    #     data = self.request.GET.get('text')
    #     categories = Category.objects.filter(title__icontains=data)
    #     # print(JsonResponse(model_to_dict(categories)))
    #     print(categories)
    #     data = CategorySerializer(categories,many=True, read_only=True)

    #     return JsonResponse(categories,safe=False)

    def get_queryset(self):
        data = self.request.GET.get('text')
        categories = Category.objects.filter(title__icontains=data)[:20]
        return categories





class CategoryDetail(generics.RetrieveAPIView):
    lookup_field = 'pk'
    serializer_class = CategorySerializer
    model = Category
    queryset = Category.objects.all()





class AddCategory(View):
    # type = question, quiz, qxa, action = remove, add, create
    def get(self, request, obj_type, obj_id, obj_action):
        if obj_type == 'quiz':
            pass
        elif obj_type == 'question':
            pass
        elif obj_type == 'qxa':
            pass

        def quizAdd(id):
            quiz = ''
            pass


class AjaxCategoryAddOrCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, quiz_id, category):
        print("Entered!")
        try:
            category = Category.objects.get(title=category)

            self.add_category(quiz_id, category)
            return Response
        except:
            user = self.request.user
            print('The category will be created')
            self.perform_create_hard(user, quiz_id, category)
            return Response

    def perform_create_hard(self, user,quiz_id, category):
        return Response

    @staticmethod
    def add_category(quiz_id, category):
        return Response




class ProfileCategory(TemplateView):
    template_name = 'quiz/categoryCreate.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obj_type"] = "profile"
        profile = self.request.user.profile
        context["objCategories"] = profile.categories.all()
        # remove the page_obj part for this profile categories
        pass
    def post(self, request):
        pass
    pass