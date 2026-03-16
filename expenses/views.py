from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . import forms, models
from events.models import Event

# Create your views here.

class EventMemberRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def get_event(self):
        if not hasattr(self, '_event_code'):
            self._event_code = self.kwargs.get('event_code')
        if not hasattr(self, '_event'):
            event = get_object_or_404(Event, code=self._event_code)
            self._event = event
        return self._event

    def test_func(self):
        user = self.request.user
        event = self.get_event()
        return user.memberships.filter(event=event).exists()
    
    def handle_no_permission(self):
        return redirect('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = self.get_event
        return context

class ExpensesView(EventMemberRequiredMixin, TemplateView):
    template_name = 'expenses/expenses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['participants'] = models.Participants.objects.filter(event = self.get_event())
        return context

class ParticipantsCreateView(EventMemberRequiredMixin, CreateView):
    form_class = forms.ParticipantsForm
    template_name = 'expenses/participants_create.html'

    def get_success_url(self):
        event = self.get_event()
        return reverse_lazy('participants_create', kwargs={'event_code': event.code})

    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['event'] = self.get_event()
        return kwargs

class ParticipantsUpdateView(EventMemberRequiredMixin, UpdateView):
    template_name = 'expenses/participants_update.html'
    model = models.Participants
    form_class = forms.ParticipantsForm
    pk_url_kwarg = 'id'
    
    def get_success_url(self):
        event = self.get_event()
        return reverse_lazy('expenses', kwargs = {'event_code': event.code})
    
    def get_queryset(self):
        return super().get_queryset().filter(event=self.get_event())
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['event'] = self.get_event()
        kwargs['update_object'] = True
        return kwargs

class ParticipantsListView(EventMemberRequiredMixin, ListView):
    model = models.Participants
    template_name = 'expenses/participant_list.html'
    context_object_name = 'participants'
    paginate_by = 2

    def get_queryset(self):
        return super().get_queryset().filter(event=self.get_event())

class ParticipantsDeleteView(EventMemberRequiredMixin, View):
    def post(self, request, event_code):
        self._event_code = event_code
        event = self.get_event()
        data = request.POST
        delete_participant_id = int(data.get('delete_participant'))
        page_name = data.get('page_name')
        if delete_participant_id is not None and event.participants.filter(id=delete_participant_id).exists():
            models.Participants.objects.filter(id=delete_participant_id).first().delete()
            if page_name == 'participant_list':
                return redirect('participants_list', event_code=event_code)
        return redirect('expenses', event_code=event_code)
