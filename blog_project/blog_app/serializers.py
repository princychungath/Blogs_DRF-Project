from rest_framework import serializers
from .models import User,Post,Comment

class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    def save(self):
        register = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password should match'})
        register.set_password(password)
        register.save()
        return register


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username']

class PostSerializer(serializers.ModelSerializer):
    author=UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id','author', 'title', 'content', 'image','created_at','updated_at']


class CommentSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'user','post' ,'content', 'created_at']


class PostviewSerializer(serializers.ModelSerializer):
    author=UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['author', 'title', 'content', 'image','created_at']


class CommentViewSerializer(serializers.ModelSerializer):
    post=PostviewSerializer(read_only=True)
    user=UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'user','post' ,'content', 'created_at']





class AdminRegisterSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField(default=True, write_only=True)
    is_staff = serializers.BooleanField(default=True, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "password2", "is_superuser", "is_staff"]

    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        is_superuser = self.validated_data['is_superuser']
        is_staff = self.validated_data['is_staff']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords should match'})

        user = User(
            username=username,
            email=email,
            is_superuser=is_superuser,
            is_staff=is_staff
        )
        user.set_password(password)
        user.save()
        return user