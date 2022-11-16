from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from django.views.generic.base import TemplateView, View, TemplateResponseMixin

from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView, DeleteView, CreateView
from django.views.generic.list import ListView
from room.forms import StudyRoomForm, AnnouncementForm
from room.models import StudyRoom
from core.models import Profile
from quiz.models import Quiz
from django.contrib.auth.models import User

from django.http import HttpResponseNotFound, JsonResponse
from django.core.paginator import Paginator


from django.utils.text import slugify


#serializers

from quiz.serializers import QuizSerializer
from q.serializers import QSerializer
from question.serializers import FourChoicesQuestionSerializer, TrueOrFalseQuestionSerializer
from .serializers import *
# Create your views here.

# DjangoJSONEncoder

"""
The home page will contain navigation links to the members, questions, four and true or false question
Whenever a link is clicked, an ajax request will fetch a related data and display them in the html document

"""


"""
Add a button to add any question, fourchoicesquestion, trueorfalsequestion to the studyroom later and add save to favourites
"""



def _checkCredibility(user, members):
    if user not in members:
        # use a json response here 
        # instead
        return HttpResponseNotFound()






class StudyRoomPage(DetailView):
    model = StudyRoom
    template_name='room/roompage.html'
    context_object_name='room'

    # def get_object(self):
    #     return self.model.objects.prefetch_related('members','quizzes', 'questions', 'fourChoicesQuestions', 'trueOrFalseQuestions').get(id=self.kwargs['room_id'])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        _checkCredibility(user, context['room'].members.all())
        context['page'] = 'quiz'
        context['profile'] = Profile.objects.get(user=user)
        context['quiz'] = Quiz.objects.get(id=5)
        return context


    def get(self, request, room_id, slug):
        return super(StudyRoomPage, self).get(request, room_id, slug)




class StudyRoomQuizList(View):
    def get(self, request, room_id):
        print("Started")
        room = StudyRoom.objects.prefetch_related('quizzes').get(id=room_id)
        quizzes = room.quizzes.all()
        # print(quizzes)
        # create pagination
        p = Paginator(quizzes, 1)
        page = self.request.GET.get('page')
        quizzes = p.get_page(page)
        print(quizzes)
        quizzes = RoomQuizSerializer(quizzes, many=True, read_only=True).data
        # print(quizzes)

        return JsonResponse(quizzes, safe=False)



class RoomMembers(View):
    def get(self, request, room_id):
        print('started')
        user = self.request.user
        room = StudyRoom.objects.prefetch_related('members').get(id=room_id)
        # _checkCredibility(user, room.members.all())
        # create a serializer for all the objects that will be needed in this section
        return JsonResponse({"members":room.members.all()})




class RoomQuestions(View):
    def get(self, request, room_id):
        user = self.request.user
        room = StudyRoom.objects.prefetch_related('questions', 'members').get(id=room_id)
        # _checkCredibility(user, room.members.all())
        questions = room.questions.all()        
        # questions = RoomQuestionSerializer(questions, many=True, read_only=True).data
        # print(questions)
        p = Paginator(questions, 1)
        page = self.request.GET.get('page')
        questions = p.get_page(page)
        questions = RoomQuestionSerializer(questions, many=True, read_only=True).data
        # print(quizzes)

        return JsonResponse(questions, safe=False)





class RoomFourChoicesQuestions(View):
    def get(self, request, room_id):
        user = self.request.user
        room = StudyRoom.objects.prefetch_related('fourChoicesQuestions', 'members').get(id=room_id)
        # _checkCredibility(user, room.members.all())
        questions = room.fourChoicesQuestions.all()
        # questions = RoomFourChoicesQuestionSerializer(questions, many=True, read_only=True).data

        p = Paginator(questions, 1)
        page = self.request.GET.get('page')
        questions = p.get_page(page)
        questions = RoomFourChoicesQuestionSerializer(questions, many=True, read_only=True).data
        # print(quizzes)

        # combine both the four and true of false question inside one query
        return JsonResponse(questions, safe=False)



class RoomTrueOrFalseQuestions(View):
    def get(self, request, room_id):
        user = self.request.user
        room = StudyRoom.objects.prefetch_related('trueOrFalseQuestions', 'members').get(id=room_id)
        # _checkCredibility(user, room.members.all())
        questions = room.trueOrFalseQuestions.all()
        # questions = RoomTrueOrFalseQuestionSerializer(questions, many=True, read_only=True).data
        p = Paginator(questions, 1)
        page = self.request.GET.get('page')
        questions = p.get_page(page)
        questions = RoomTrueOrFalseQuestionSerializer(questions, many=True, read_only=True).data
        # print(quizzes)

        return JsonResponse(questions, safe=False)





# all these views will remain the same

# add list study view here

class CreateStudyRoom(CreateView):
    model = StudyRoom
    success_url = '' #add the success url later
    template_name = 'room/create_room.html'
    # context_object_name = 'room'
    form_class = StudyRoomForm

    def form_valid(self, form):
        user = self.request.user
        name = form.cleaned_data.get('name')
        room = StudyRoom.objects.create(name=name,
            user=user
            )
        room.members.add(user)
        room.slug = slugify(room.name)
        room.save()
        # return the absolute url instead of id and slug
        return JsonResponse({"action":"created", "id":"room.id", "slug":"room.slug"})# redirect the user to the study room



class LeaveStudyRoom(View):
    def get(self, request, room_id):
        user = self.request.user
        room = StudyRoom.objects.prefetch_related('members').get(id=room_id)
        if user in room.members.all():
            room.members.remove(user)
        return JsonResponse({"action":"removed"})



class JoinStudyRoom(View):
    def get(self, request, room_id):
        user = self.request.user
        room = StudyRoom.objects.prefetch_related('members').get(id=room_id)
        if room.members.count() > 11:
            return JsonResponse({"action":"closed"})
            
        if user not in room.members.all():
            room.members.add(user)

        return JsonResponse({"action": "joined"})



def _validateGroupCreator(user, creator):
    if user != creator:
        return JsonResponse({"action":"rejected"})




# add remove to all the questions
class AddGroupMember(View):
    def get(self, request, username, room_id):
        # check if the username already exists
        user = self.request.user
        member = User.objects.get(username=username)
        room = StudyRoom.objects.select_related('user').prefetch_related('members').get(id=room_id)

        _validateGroupCreator(user, room.user)

        room.members.add(member)

        return JsonResponse({"action":"removed"})



class RemoveGroupMember(View):
    def get(self, request, member_id, room_id):
        user = self.request.user
        member = User.objects.get(id=member_id)
        room = StudyRoom.objects.select_related('user').prefetch_related('members').get(id=room_id)

        _validateGroupCreator(user, room.user)

        room.members.remove(member)

        return JsonResponse({"action":"removed"})



"""
class MakeAnnouncements(FormView):
    template_name='room/make_announcement.html'
    form_class = AnnouncementForm
    def get(self, request, room_id):
        room = StudyRoom.objects.select_related('user').get(id=room_id)
        user = self.request.user
        if user != room.user:
            return JsonResponse({"action":"rejected"})
        # add an announcements model
        # add an indicator if the announcements are made
        # users won't see the indicator twice
"""





# Add search later