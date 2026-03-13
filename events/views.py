from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from . import forms

# Create your views here.

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'events/home.html'
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        memberships = user.memberships.all()
        context_data['memberships'] = memberships.order_by('-joined_at')[:6]
        return context_data
    
class CreateEventView(LoginRequiredMixin, CreateView):
    form_class = forms.CreateEventForm
    template_name = 'events/create_event.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = self.request.user
        form.instance.creator = user
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs



# events = models.Event.objects.all()
# for event in events:
#     print(event.title)
#     print(event.code)
#     print(event.creator.first_name)
#     print('------------------------------------')
#     # event.delete()