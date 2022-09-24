from account import models
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
        extra_kwargs = {
            'is_active': {'write_only': True},
            'is_staff': {'write_only': True},
            'password': {'write_only': True}
        }