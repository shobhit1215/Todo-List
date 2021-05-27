from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Task
from django.template import loader
# we can import Class Views from here
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

#These two views are used to check authentication in functional and class based views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


#applied tasklist and task detail with functional views 

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def self_success_url(self):
        return reverse_lazy('task')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)

    def get(self, *args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(RegisterPage,self).get(*args,**kwargs)


# @login_required
# def tasklist(request):
#     task_list = Task.objects.all()
#     template=loader.get_template('base/index.html')
#     context={
#         'task_list':task_list,
#     }
#     return HttpResponse(template.render(context,request))

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'task_list'
#this function displays user specifiec data.We override this method

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['task_list'] = context['task_list'].filter(user=self.request.user)
        context['count'] = context['task_list'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
             context['task_list'] = context['task_list'].filter(title__startswith=search_input)
        context['search_input']=search_input
        return context

@login_required
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


class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('task')
# This function set the default user which is loged in .We override this method
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ['title','description','complete']
    success_url = reverse_lazy('task')

# In taskdelete view template name is modelname_confirm_delete.html.This template has a form which confirms delete operations

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task')




