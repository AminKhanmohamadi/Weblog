from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import  generic
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
class SingUpView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/singup.html'
    success_url = reverse_lazy('login')