from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpRequest
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.contrib import messages
from . import forms, models
from accounts.views import calculate_retry_available_at

# Create your views here.

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'events/home.html'
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        memberships = user.memberships.all()
        context_data['memberships'] = memberships.order_by('-joined_at')[:6]
        join_requests = user.join_requests.all()
        context_data['join_requests'] = join_requests.order_by('-requested_at')[:4]
        return context_data

class CreateEventView(LoginRequiredMixin, CreateView):
    form_class = forms.CreateEventForm
    template_name = 'events/create_event.html'
    
    def get_success_url(self):
        return reverse_lazy(
            'create_event_success',
            kwargs={'event_code': self.object.code}
        )

    def form_valid(self, form):
        user = self.request.user
        form.instance.creator = user
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class CreateJoinRequestView(LoginRequiredMixin, View):
    def get(self, request):
        template_name = 'events/create_join_request.html'
        form = forms.CreateJoinRequestForm()
        return render(request, template_name, {'form':form})
    def post(self, request:HttpRequest):
        form = forms.CreateJoinRequestForm(request.POST)
        template_name = 'events/create_join_request.html'

        if not form.is_valid():
            return render(request, template_name, {'form':form})
        
        event_code = form.cleaned_data.get('event_code')
        user = request.user
        now = datetime.now()
        
        if user.memberships.filter(event__code=event_code).exists():
            form.add_error('event_code', 'You are already a member of this event.')
            return render(request, template_name, {'form':form})
        
        if user.join_requests.filter(event__code=event_code).exists():
            form.add_error('event_code', 'You’ve already sent a request to join this event.')
            return render(request, template_name, {'form':form})


        # Check for existing session data for the event code retry delay.
        retry_ts = request.session.get('retry_available_at')
        failed_attempts = request.session.get('request_failed_attempts')
        if retry_ts is not None and failed_attempts is not None:
            retry_available_at = datetime.fromtimestamp(retry_ts)
            
        else:
            self.request.session['request_failed_attempts'] = 0
            self.request.session['retry_available_at'] = (now - timedelta(minutes=1)).timestamp() # minutes
            retry_available_at = now - timedelta(minutes=1)

        if retry_available_at < now:
            retry_available_at = calculate_retry_available_at(request.session.get('request_failed_attempts'))

            
            if models.Event.objects.filter(code=event_code).exists():
                request.session.pop('retry_available_at', None)
                request.session.pop('request_failed_attempts', None)
                
                event = models.Event.objects.filter(code=event_code).first()
                models.EventJoinRequest.objects.create(user=user, event=event)

                return redirect('create_join_request_success', event_title = event.title)
            
            elif retry_available_at > now: # If the retry delay changes, it will be stored in the session and the user cannot retry for a while.
                self.request.session['retry_available_at'] = retry_available_at.timestamp()
                form.add_error('event_code', 'Too many attempts.')
                self.request.session['request_failed_attempts'] += 1

            else:
                form.add_error('event_code', 'The event code is incorrect')
                self.request.session['request_failed_attempts'] += 1

        else: # Return an error if the user has exceeded the retry limit. 
            minutes = int((retry_available_at - now).total_seconds() / 60) + 1
            form.add_error('event_code', f'Too many attempts. Please try again in {minutes} minutes.')
        return render(request, template_name, {'form':form})

class EventView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'events/event.html'

    def test_func(self):
        user = self.request.user
        event_code = self.kwargs.get('event_code')
        event = get_object_or_404(models.Event, code=event_code)
        return user.memberships.filter(event=event).exists()
    
    def handle_no_permission(self):
        return redirect('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_code = self.kwargs.get('event_code')
        event = get_object_or_404(models.Event, code=event_code)
        user = self.request.user
        membership = user.memberships.filter(event=event).first()
        if event.creator == user:
            join_requests = models.EventJoinRequest.objects.filter(event=event).all()
            members_list = event.memberships.all()
            context['join_requests'] = join_requests.order_by('-requested_at')[:4]
            context['members_list'] = members_list.order_by('joined_at')[:6]

        context['membership'] = membership
        context['event'] = event
        return context

class JoinRequestHandlerView(LoginRequiredMixin, View):
    def post(self, request:HttpRequest, request_id):
        join_request = get_object_or_404(models.EventJoinRequest, id = request_id)
        event = join_request.event
        btn_action = request.POST.get('btn_action')
        page = request.POST.get('page')
        context_data = {}
        # context_data['accept_request'] = False

        # event join requests
        if event.creator == request.user:
            if btn_action == 'reject':
                join_request.delete()
            elif btn_action == 'accept':
                models.EventMembership.objects.create(
                    event=event,
                    user=join_request.user
                    )
                join_request.delete()
                # if page == 'event':
                #     context_data['accept_request'] = True
            if page == 'event':
                context_data['join_requests'] = models.EventJoinRequest.objects.filter(event=event).all().order_by('-requested_at')[:4]
                return render(request, 'events/includes/event/event_join_requests.html', context=context_data)
            elif page == 'event_join_request_list':
                context_data['join_requests'] = models.EventJoinRequest.objects.filter(event=event).all().order_by('-requested_at')
                return render(request, 'events/includes/event_join_request_list/event_join_requests.html', context=context_data)
        
        # user join request
        elif join_request.user == self.request.user:
            if btn_action == 'remove':
                join_request.delete()
            if page == 'home':
                context_data['join_requests'] = request.user.join_requests.all().order_by('-requested_at')[:4]
                return render(request, 'events/includes/home/join_requests.html', context=context_data)
            elif page == 'join_request_list':
                context_data['join_requests'] = request.user.join_requests.all().order_by('-requested_at')
                return render(request, 'events/includes/join_request_list/join_requests.html', context=context_data)
        return redirect('home')

class EventMembershipHandlerView(LoginRequiredMixin, View):
    def post(self, request:HttpRequest, member_id):
        membership = get_object_or_404(models.EventMembership, id = member_id)
        event = membership.event
        if event.creator == request.user and membership.user != event.creator:
            if request.POST.get('admin') == '':
                membership.can_edit_event_info = True
                membership.save()
            elif request.POST.get('member') == '':
                membership.can_edit_event_info = False
                membership.save()
            elif request.POST.get('remove') == '':
                membership.delete()
            return redirect('event', event_code=event.code)
        return redirect('home')

class EventListView(LoginRequiredMixin, ListView):
    template_name = 'events/event_list.html'
    model = models.EventMembership
    context_object_name = 'memberships'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.select_related('user').filter(user=user).order_by('-joined_at')
        return queryset

class JoinRequestListView(LoginRequiredMixin, ListView):
    template_name = 'events/join_request_list.html'
    model = models.EventJoinRequest
    context_object_name = 'join_requests'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        queryset = queryset.select_related('user').filter(user=user).order_by('-requested_at')
        return queryset

class EventJoinRequestListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'events/event_join_request_list.html'
    model = models.EventJoinRequest
    context_object_name = 'join_requests'
    paginate_by = 20

    def get_event(self):
        if not hasattr(self, '_event'):
            event_code = self.kwargs.get('event_code')
            self._event = get_object_or_404(models.Event, code=event_code)
        return self._event

    def get_queryset(self):
        queryset = super().get_queryset()
        event = self.get_event()
        queryset = queryset.select_related('event').filter(event=event).order_by('-requested_at')
        return queryset
    
    def test_func(self):
        user = self.request.user
        event = self.get_event()
        return user.memberships.filter(event=event).exists()
    
    def handle_no_permission(self):
        return redirect('home')

class EventMembersListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'events/event_members_list.html'
    model = models.EventMembership
    context_object_name = 'members_list'
    paginate_by = 20

    def get_event(self):
        if not hasattr(self, '_event'):
            event_code = self.kwargs.get('event_code')
            self._event = get_object_or_404(models.Event, code=event_code)
        return self._event

    def get_queryset(self):
        queryset = super().get_queryset()
        event = self.get_event()
        queryset = queryset.select_related('event').filter(event=event).order_by('joined_at')
        return queryset
    
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        event = self.get_event()
        context_data['event_creator'] = event.creator
        return context_data
    
    def test_func(self):
        user = self.request.user
        event = self.get_event()
        return user.memberships.filter(event=event).exists()
    
    def handle_no_permission(self):
        return redirect('home')

class CreateEventSuccessView(LoginRequiredMixin, TemplateView): 
    template_name = 'events/create_event_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_code = self.kwargs.get('event_code')
        event = get_object_or_404(models.Event, code=event_code)
        context["event"] = event
        return context

class CreateJoinRequestSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'events/create_join_request_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_title"] = self.kwargs.get('event_title')
        return context

# events = models.Event.objects.all()
# for event in events:
#     print(event.title)
#     print(event.code)
#     print(event.creator.first_name)
#     print('------------------------------------')
#     # event.delete()