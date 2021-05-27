from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # urls for basic CRUD functionalities
    path('login/',views.CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='task'),name='logout'),
    path('register/',views.RegisterPage.as_view(),name='register'),
    path('',views.TaskList.as_view(),name='task'),
    path('task/<int:id>',views.taskdetail,name='detail'),
    path('create-task/',views.TaskCreate.as_view(),name='task-create'),
    path('update-task/<int:pk>',views.TaskUpdate.as_view(),name='update-task'),
    path('delete-task/<int:pk>',views.TaskDelete.as_view(),name='delete-task'),
]