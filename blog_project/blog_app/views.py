from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSignUpSerializer,PostSerializer,CommentSerializer,AdminRegisterSerializer,CommentViewSerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
from rest_framework import generics
from .models import Post,Comment
from django_filters.rest_framework import DjangoFilterBackend



#-------------------User Authentication & email sending ------------------#

class RegisterUser(APIView):
    def post(self, request, format=None):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            email_to=[customer.email]
            subject= 'User Registration'
            message = "Dear,\n\n Your registration was successfully completed \n\nThank You"
            send_mail(
                subject,message,settings.DEFAULT_FROM_EMAIL,email_to)
            return Response({"message": "User created."}) 
        else:
            return Response(serializer.errors)

#-------------------Blog Create, update, Delete, List, Detail ------------------#

class BlogCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def post(self, request, *args, **kwargs):
        request.data['created_user'] = request.user.id
        response = super().post(request, *args, **kwargs)
        return Response({"message": "New Post created"})


class BlogUpdate(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
           return Response({"message":"You don't have the permission to update this Post"})
        return super().patch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
           return Response({"message":"You don't have the permission to update this Post"})
        return super().put(request, *args, **kwargs)
        

class BlogDestroy(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author != request.user:
            return Response({"message": "You don't have the permission to delete this Post"})
        response = super().delete(request, *args, **kwargs)
        return Response({'message': 'Post is deleted'})


class Postlist(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class=PostSerializer
    permission_classes = [AllowAny]


class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class=PostSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            instance = self.queryset.get(pk=pk)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response({"message": "Post not found."})



#-------------------Comment list,Detail,Create,Update,delete ------------------#

class CommentList(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentViewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post']

class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentUpdate(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
           return Response({"message":"You don't have the permission to update this Comment"})
        return super().patch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
           return Response({"message":"You don't have the permission to update this Comment"})
        return super().put(request, *args, **kwargs)
        

class CommentDestroy(generics.DestroyAPIView):
    queryset =Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response({"message": "You don't have the permission to delete this Comment"})
        response = super().delete(request, *args, **kwargs)
        return Response({'message': 'Comment is deleted'})




#-------------------Admin Registration Postlist & detail view & delete post------------------#

class Admin_registerView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = AdminRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Admin User created."})
        else:
            return Response(serializer.errors)


class Admin_PostlistDeatilView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class=PostSerializer
    permission_classes=[IsAdminUser]
    authentication_classes=[JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']


class Admin_BlogDestroy(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class=PostSerializer
    permission_classes=[IsAdminUser]
    authentication_classes=[JWTAuthentication]


    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({'message': 'Post is deleted'})


class Admin_CommentlistDeatilView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes=[IsAdminUser]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post']


class Admin_CommentDestroy(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class=CommentSerializer
    permission_classes=[IsAdminUser]
    authentication_classes=[JWTAuthentication]


    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        return Response({'message': 'Comment is deleted'})


