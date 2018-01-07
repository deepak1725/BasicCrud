from django.contrib.auth.models import User
from api.serializers import ChatRecordsSerializer, UserChannelsSerializer, AllChannelSerializer
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework import status
from django.http import HttpResponse
from users.models import UserChatRecords,UserChannels, FriendChannels, AllChannels, GroupUsers
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
import random, string, types
from rest_framework import generics
from django.core import serializers



class UsersChatRecoredsViewSet(viewsets.ModelViewSet):
    permission_classes = ''
    authentication_classes = ''
    queryset = UserChatRecords.objects.all()
    serializer_class = ChatRecordsSerializer

    def retrieve(self, request, *args, **kwargs):
        # pk --> userId
        userId = kwargs['pk']
        userChatObj = UserChatRecords.objects.filter(user = userId).first()
        serializer = ChatRecordsSerializer(userChatObj)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        userId = request.data['user']
        user = UserChatRecords.objects.filter(user=userId).first()

        if (user):
            serializer = ChatRecordsSerializer(user)
            return Response(serializer.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserChannelsViewSet(viewsets.ModelViewSet):
    queryset = UserChannels.objects.all()
    serializer_class = UserChannelsSerializer
    permission_classes = ''
    authentication_classes = ''


    def retrieve(self, request, *args, **kwargs):
        instance = UserChannels.objects.filter(user_id=kwargs['pk']).first()
        serializer = self.get_serializer(instance)
        message = 'Data Successfully fetched'
        if not serializer.data['user']:
            message = "No User Found"
        responseData = {
            'message' : message,
            'data': serializer.data,
            'error' : None
        }
        return Response(responseData,  status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        response = super(UserChannelsViewSet, self).create(request, args, kwargs)
        message = 'Channel Successfully created'

        responseData = {
            'message': message,
            'data': response.data,
            'error': None
        }
        return Response(responseData, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        response = super(UserChannelsViewSet, self).list(request, args, kwargs)
        message = 'Data Successfully fetched'

        responseData = {
            'message': message,
            'data': response.data,
            'error': None
        }
        return Response(responseData, status=status.HTTP_200_OK)



class GetChannelNameViewSet(APIView):
    permission_classes = ''
    authentication_classes = ''

    def get(self, request, *args, **kw):

        condition = True
        result=None

        while condition:
            result = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            condition = FriendChannels.objects.filter(channel=result).exists()

        responseData = {
            'message': 'Channel Name Successfully Created.',
            'data': {'name':result},
            'error': None
        }
        return Response(responseData, status=status.HTTP_200_OK)

class UserDetailsViewSet(APIView):
    permission_classes = ''
    authentication_classes = ''

    def get(self, request, *args, **kw):
        arg_2 = request.GET.get('username')
        arg_1 = request.GET.get('id')
        message = 'Invalid or missing username.'
        data = {}

        if arg_1:
            message = 'User Found'
            user = User.objects.get(id = arg_1)
            data = {'id':user.id, 'first_name' : user.first_name, 'last_name' : user.last_name, 'username': user.username}

        elif isinstance(arg_2, str):
            user = User.objects.get_by_natural_key(arg_2)

            message = 'User Details Successfully fetched'
            data = {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'username': user.username}

        responseData = {
            'message': message,
            'data': data,
            'error': None
        }
        return Response(responseData, status=status.HTTP_200_OK)


class AllChannelsViewSet(viewsets.ModelViewSet):
    permission_classes = ''
    authentication_classes = ''
    queryset = AllChannels.objects.all()
    serializer_class = AllChannelSerializer

    def retrieve(self, request, *args, **kwargs):

        instance = AllChannels.objects.filter(users__user__id=kwargs['pk']).all()

        print(instance)

        serializer = self.get_serializer(instance)
        # return Response(serializer.data)

        message = 'Data Retrieved Successfully'
        # queryset =
        responseData = {
            'message': message,
            'data': serializer.data,
            'error': None
        }
        return Response(responseData, status=status.HTTP_201_CREATED)


    def create(self, request, *args, **kwargs):
        response = super(AllChannelsViewSet, self).create(request, args, kwargs)
        message = 'Channel Successfully created'

        responseData = {
            'message': message,
            'data': response.data,
            'error': None
        }
        return Response(responseData, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        response = super(AllChannelsViewSet, self).update(request, args, kwargs)
        message = 'Channel Successfully Updated'

        responseData = {
            'message': message,
            'data': response.data,
            'error': None
        }
        return Response(responseData, status=status.HTTP_201_CREATED)


class GetUserChannels(generics.RetrieveAPIView):
    permission_classes = ''
    authentication_classes = ''
    # serializer_class = AllChannelSerializer

    def get(self, request,*args, **kw):
        instance = AllChannels.objects.filter(users__user__id=kw['pk'])
        print(instance)
        serializer = serializers.serialize("json", instance)
        return Response(serializer)
        #
        # print(user)
        # responseData = {
        #     'message': 'Channel Name Successfully Created.',
        #     'data': {'user':user},
        #     'error': None
        # }
        # responseData = super(GetUserChannels,self).get(self,request,args,kw)
        # return Response(responseData, status=status.HTTP_200_OK)
