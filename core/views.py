from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from . import models, forms

# Create your views here.
class HomeView(TemplateView):
    template_name = 'core/home.html'

class ContactView(CreateView):
    template_name = 'core/contact.html'
    form_class = forms.ContactMessageForm
    success_url = reverse_lazy('contact')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_settings = models.SiteSettings.objects.filter(is_active = True).first()
        context['site_settings'] = site_settings
        user = self.request.user
        if user.is_authenticated:
            form = forms.ContactMessageForm(initial={'email': user.email})
        else:
            form = forms.ContactMessageForm()
        context['form'] = form
        return context
    
class AboutView(TemplateView):
    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_settings'] = models.SiteSettings.objects.filter(is_active = True).first()
        return context