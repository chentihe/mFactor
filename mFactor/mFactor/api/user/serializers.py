from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from mFactor.api.user.models import UserProfile, DeliveryInfo, UserBody

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('phone', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 6,
                'max_length': 127
            },
            'phone': {
                'validators': [UniqueValidator(queryset=UserProfile.objects.all())]
            }
        }

class DeliveryInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryInfo
        fields = ('name', 'address', 'phone')

class UserBodySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserBody
        fields = '__all__'

class PasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=127)