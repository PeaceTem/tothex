from rest_framework import generics
from rest_framework.response import Response



from .models import *

from .serializers import *




class StudyRoomList(generics.ListAPIView):
    queryset = StudyRoom.objects.all()
    serializer_class = StudyRoomSerializer
    # permission_classes = [permissions.IsAdminUser]




class StudyRoomDetail(generics.RetrieveAPIView):
    queryset = StudyRoom.objects.all()
    serializer_class = StudyRoomSerializer
    lookup_field ='pk'


    def get(self, request, pk, slug):
        return super(StudyRoomDetail, self).get(request, pk, slug)




class RoomMembers(generics.ListAPIView):
    queryset = RoomMember.objects.all()
    serializer_class = RoomMemberSerializer

