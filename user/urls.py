from django.urls import path,include
from.import views
from user.views import DetailsChangeView, HomeView, PasswordChangeView,SignUpView,LoginView,SettingsView,LogoutView,CreatePostView,CommentPostView,PasswordChangeView

urlpatterns = [
    path('', HomeView.as_view(), name = 'HomeView'),
    path('LoginView/', LoginView.as_view(), name = 'LoginView'),
    path('SignUpView/',SignUpView.as_view(), name = 'SignUpView' ),
    path('SettingsView/', SettingsView.as_view(), name = 'SettingsView'),
    path('LogoutView/', LogoutView.as_view(), name = 'LogoutView'),
    path('social_auth/', include('social_django.urls', namespace = 'social')),
    path('users_list/', views.users_list, name = 'users_list'),
    path('CreatePostView/', CreatePostView.as_view(), name = 'CreatePostView'),
    path('like/<int:id>/', views.like , name = 'like'),
    path('CommentPostView/<int:id>/', CommentPostView.as_view(), name = 'CommentPostView'),
    path('follow/<int:id>/', views.follow , name = 'follow'),
    path('followback/<int:id>/', views.followback, name = 'followback'),
    path('delete_request/<int:id>/',views.delete_request, name = 'delete_request'),
    path('unfriend/<int:id>/', views.unfriend, name = 'unfriend'),
    path('friendslist/<int:id>/',views.friendslist, name = 'friendslist'),
    # path('FollowListView/<int:id>/',FollowListView.as_view(), name = 'FollowListView')
    path('PasswordChangeView/', PasswordChangeView.as_view(), name = 'PasswordChangeView'),
    path('DetailsChangeView/', DetailsChangeView.as_view(), name= 'DetailsChangeView'),
    path('user_profile_view/<int:id>/',views.user_profile_view, name = 'user_profile_view'),
    path('start_chat/<int:id>/', views.start_chat, name= 'start_chat'),
    path('search_function/', views.search_function, name='search_function')
   
   
]