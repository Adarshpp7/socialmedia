from django.urls import path,include
from.import views
from admin1.views import AdLoginView, AdLogoutView


urlpatterns = [
    path('', AdLoginView.as_view(), name = 'AdLoginView'),
    path('home/', views.home, name = 'home'),
    path('user_list/', views.user_list, name = 'user_list'),
    path('user_block/<int:id>/', views.user_block, name = 'user_block'),
    path('AdLogoutView/', AdLogoutView.as_view(), name= 'AdLogoutView')
 
   
]