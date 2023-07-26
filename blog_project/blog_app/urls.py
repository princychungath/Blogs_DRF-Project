from django.urls import path
from blog_app import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns=[
    path('register/',views.RegisterUser.as_view(),name="register"),
    path('login/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    

    path('blog/create/',views.BlogCreateView.as_view(), name='blog-create'),
    path('update/<int:pk>',views.BlogUpdate.as_view(),name="blog-update"),
    path('delete/<int:pk>',views.BlogDestroy.as_view(),name="blog-destroy"),
    path('blog/list/',views.Postlist.as_view(), name='blog-list'),
    path('blog/detail/<int:pk>',views.PostDetail.as_view(), name='blog-detail'),


    path('comments/add/',views.CommentCreateView.as_view(), name='comment-create'),
    path('comments/list',views.CommentList.as_view(),name="comment-list"),
    path('update/comment/<int:pk>',views.CommentUpdate.as_view(),name="comment-update"),
    path('delete/comment/<int:pk>',views.CommentDestroy.as_view(),name="comment-destroy"),

    path('reg/admin',views.Admin_registerView.as_view(), name='register-admin'),
    path('Blog/list/admin',views.Admin_PostlistDeatilView.as_view(),name='bloglistview-admin'),
    path('Blog/delete/admin/<int:pk>',views.Admin_BlogDestroy.as_view(),name='blogdelete-admin'),
    path('comments/view/admin/',views.Admin_CommentlistDeatilView.as_view(),name='commentlist-admin'),
    path('comments/delete/admin/<int:pk>',views.Admin_CommentDestroy.as_view(),name='commentdelete-admin'),


]