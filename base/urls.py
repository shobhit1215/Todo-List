from django.urls import path
from . import views

urlpatterns = [
    # urls for basic CRUD functionalities
    path('',views.tasklist,name='task'),
    path('task/<int:id>',views.taskdetail,name='detail'),
    path('create-task/',views.TaskCreate.as_view(),name='task-create'),
    path('update-task/<int:pk>',views.TaskUpdate.as_view(),name='update-task'),
    path('delete-task/<int:pk>',views.TaskDelete.as_view(),name='delete-task'),
]