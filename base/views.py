from django.shortcuts import render
from django.http import HttpResponse
from .models import Task
from django.template import loader
# we can import Class Views from here
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

#applied tasklist and task detail with functional views 

def tasklist(request):
    task_list = Task.objects.all()
    template=loader.get_template('base/index.html')
    context={
        'task_list':task_list,
    }
    return HttpResponse(template.render(context,request))

def taskdetail(request,id):
    task = Task.objects.get(id=id)
    template =loader.get_template('base/detail.html')
    context={
        'task':task,
    }
    return HttpResponse(template.render(context,request))

#CRUD functionalities with Class based views
# Refer https://www.dennisivy.com/post/django-class-based-views/ for detailed explanaition of this
# See textutils/food app project for its alternatives

#TaskCreate and TaskUpdate takes same template by default whose name is modelname_form.html.In these views form is automatically created for defined model


class TaskCreate(CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('task')

class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('task')

# In taskdelete view template name is modelname_confirm_delete.html.This template has a form which confirms delete operations

class TaskDelete(DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task')




