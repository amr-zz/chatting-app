from rest_framework import serializers
from .models import MyUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'profile_image'
        ]

class UserRegistrationSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(default='profile_images/default.jpg')
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password', 'password2','first_name','last_name','profile_image']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')

        user = MyUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            profile_image = validated_data.get('profile_image')
        )
        return user