from django.urls import path
from .views import UserList, UserLogin, UserLogout, UserRetrieveUpdateDestroy, UserRegister


app_name = 'users'

urlpatterns = [
    path('<int:pk>/', UserRetrieveUpdateDestroy.as_view(), name='retrieve_update_destroy'),
    path('register', UserRegister.as_view(), name='user_register'),
    path('login', UserLogin.as_view(), name='user_login'),
    path('logout', UserLogout.as_view(), name='user_logout'),
    path('', UserList.as_view(), name='list_create'),
] 
 