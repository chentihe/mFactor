from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import update_session_auth_hash
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from mFactor.api.user.models import UserProfile, DeliveryInfo, UserBody
from mFactor.api.user.serializers import UserSerializer, DeliveryInfoSerializer, UserBodySerializer, PasswordSerializer
from mFactor.api.user.service import DeliveryInfoService
from mFactor.api.user.permissions import IsUserOrReadOnly

class UserCreateView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class UserView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if bool(request.user.is_anonymous):
            return Response()

        return Response(UserSerializer(request.user).data)

class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = PasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        user.set_password(serializer.data['password'])
        user.save()

        # Password change, user is logged out, need to login again
        update_session_auth_hash(request, user)

        return Response(status=status.HTTP_200_OK)

class DeliveryInfoView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        try:
            deliveryinfo = user.deliveryinfo
        except DeliveryInfo.DoesNotExist:
            return Response({})
        
        return Response(DeliveryInfoSerializer(deliveryinfo).data)

    def post(self, request):
        serializer = DeliveryInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        DeliveryInfoService.delete_by_user(request.user)

        serializer.save(user=request.user)

        return Response(status=status.HTTP_201_CREATED)

class UserBodyCreateView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsUserOrReadOnly,)
    queryset = UserBody.objects.all()
    serializer_class = UserBodySerializer

class UserBodyRUView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsUserOrReadOnly,)
    queryset = UserBody.objects.all()
    serializer_class = UserBodySerializer