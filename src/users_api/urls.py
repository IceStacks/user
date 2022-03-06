from django.urls import path
from .views import UserList, UserDetail


app_name = 'users'

urlpatterns = [
    path('<int:pk>/', UserDetail.as_view(), name='detailcreate'),
    path('', UserList.as_view(), name='listcreate'),
] 
 