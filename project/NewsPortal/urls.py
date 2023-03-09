from django.urls import path
from .views import *


urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view()),
   path('create/', PostCreate.as_view(), name='create'),
   path('<int:pk>/update/', PostUpdate.as_view()),
   path('<int:pk>/delete/', PostDelete.as_view()),
   path('<int:pk>/UpdateUser/', UserUpdate.as_view(), name='update_user'),
   path('search/', PostListSearch.as_view(), name='post_search'),
   path('login/', LoginUser.as_view(), name='login'),
   path('logout/', logout_user, name='logout'),
   path('password_change/', User_password_change.as_view(), name='passchange'),
   path('register/', RegisterUser.as_view(), name='register'),
]