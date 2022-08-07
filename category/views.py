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







