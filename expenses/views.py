from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from events.models import Event
from django.db import transaction
from . import forms, models


# Mixins and functions
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
        context["event"] = self.get_event()
        return context

class PaymentMixin(EventMemberRequiredMixin):
    def get_expense(self):
        expense_id = self.kwargs.get('expense_id')
        if not expense_id:
            if hasattr(self, self.expense_id):
                expense_id = self.expense_id
            else:
                raise ValueError('expense_id not found')
            
        if not hasattr(self, '_expense'):
            self._expense = get_object_or_404(models.Expenses, id=expense_id)

        return self._expense

    def test_func(self):
        base_test = super().test_func()
        event = self.get_event()
        expense = self.get_expense()
        is_expense_exists = expense.event == event
        return base_test and is_expense_exists
    
    def handle_no_permission(self):
        return redirect('dashboard', event_code = self._event_code)

def create_empty_payments_for_expense(expense):
    participants = expense.event.participants.all()
    for participant in participants:
        models.ParticipantExpense.objects.create(expense = expense,participant = participant, share_amount = 0, paid_amount = 0)

def create_empty_payments_for_participant(participant):
    expenses = participant.event.expenses.all()
    for expense in expenses:
        models.ParticipantExpense.objects.create(expense = expense,participant = participant, share_amount = 0, paid_amount = 0)

def update_total_amounts(event):
    expenses = event.expenses.all()
    participants = event.participants.all()
    for expense in expenses:
        total_amount = expense.payments.aggregate(Sum('share_amount')).get('share_amount__sum') or 0
        expense.total_amount = total_amount
        expense.save()

    for participant in participants:
        total_share = participant.payments.aggregate(Sum('share_amount')).get('share_amount__sum') or 0
        total_paid = participant.payments.aggregate(Sum('paid_amount')).get('paid_amount__sum') or 0
        participant.total_paid = total_paid
        participant.total_share = total_share
        participant.save()

def create_default_currency_units(event):
    default_items = [
        ("USD", True),
        ("EUR", False),
        ("IRT", False),
    ]
    for currency, is_active in default_items:
        models.CurrencyUnit.objects.create(event = event, title = currency, is_active = is_active)
# Create your views here.
class ExpensesView(EventMemberRequiredMixin, TemplateView):
    template_name = 'expenses/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_event()
        participants = models.Participants.objects.filter(event = event).all()[:11]
        for p in participants:
            p.balance = p.total_paid - p.total_share
            print(p.full_name)
            print(p.balance)
            print('-------------')
        expenses = models.Expenses.objects.filter(event = event).all()
        context['participants'] = participants
        context['expenses'] = expenses.order_by('-expense_date', '-created_at')[:11]
        context['total_cost'] = expenses.aggregate(Sum('total_amount')).get('total_amount__sum')
        if not event.currencys.exists():
            create_default_currency_units(event)
        context['currency_unit'] = event.currencys.filter(is_active = True).first().title
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
    
    @transaction.atomic
    def form_valid(self, form):
        self.object = form.save()
        create_empty_payments_for_participant(self.object)
        return HttpResponseRedirect(self.get_success_url())

class ParticipantsUpdateView(EventMemberRequiredMixin, UpdateView):
    template_name = 'expenses/participants_update.html'
    model = models.Participants
    form_class = forms.ParticipantsForm
    pk_url_kwarg = 'id'
    
    def get_success_url(self):
        event = self.get_event()
        if self.request.GET.get('page')=='participants_list':
            return reverse_lazy('participants_list', kwargs = {'event_code': event.code})
        return reverse_lazy('dashboard', kwargs = {'event_code': event.code})
    
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
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(event=self.get_event())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_event()
        context['currency_unit'] = event.currencys.filter(is_active = True).first().title
        return context

class ParticipantsDeleteView(EventMemberRequiredMixin, View):
    def post(self, request, event_code):
        self._event_code = event_code
        event = self.get_event()
        data = request.POST
        delete_participant_id = int(data.get('delete_participant'))
        page_name = data.get('page_name')
        participant = get_object_or_404(event.participants, id = delete_participant_id)
        if participant.total_paid + participant.total_share == 0:
            participant.delete()

        if page_name == 'participant_list':
                return redirect('participants_list', event_code=event_code)
        return redirect('dashboard', event_code=event_code)

class ExpensesCreateView(EventMemberRequiredMixin, CreateView):
    template_name = 'expenses/expenses_create.html'
    form_class = forms.ExpensesForm
    
    def get_success_url(self):
        kwargs = {"event_code": self.get_event().code,
                  'expense_id': self.object.id}
        return reverse_lazy('split_payment', kwargs = kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['event'] = self.get_event()
        return kwargs
    
    @transaction.atomic
    def form_valid(self, form):
        self.object = form.save()
        create_empty_payments_for_expense(self.object)
        return HttpResponseRedirect(self.get_success_url())

class ExpensesUpdateView(EventMemberRequiredMixin, UpdateView):
    template_name = 'expenses/expenses_edit.html'
    model = models.Expenses
    form_class = forms.ExpensesForm
    pk_url_kwarg = 'id'
    
    def get_success_url(self):
        event = self.get_event()
        id = self.kwargs.get('id')
        return reverse_lazy('split_payment', kwargs = {'event_code': event.code, 'expense_id': id})
    
    def get_queryset(self):
        return super().get_queryset().filter(event=self.get_event())
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['event'] = self.get_event()
        kwargs['update_object'] = True
        return kwargs

class SplitPaymentView(PaymentMixin, View):
    def create_forms(self, post_data = None):
        expense = self.get_expense()
        payments = expense.payments.all()

        forms_by_participant = []
        for payment in payments:
            participant = payment.participant
            participant_expense_form = forms.ParticipantExpenseForm(post_data, prefix = f'p{participant.id}', instance = payment)
            forms_by_participant.append((participant, participant_expense_form))
        return forms_by_participant
    
    def is_all_forms_valid(self, forms_by_participant):
        paid_sum = 0
        share_sum = 0
        for form in forms_by_participant:
            participant_expense_form = form[1]
            if not participant_expense_form.is_valid():
                return False
            paid_sum += float(participant_expense_form.cleaned_data.get('paid_amount'))
            share_sum += float(participant_expense_form.cleaned_data.get('share_amount'))
        if paid_sum != share_sum:
            return False
        return True
    

    
    @transaction.atomic
    def save_all_forms(self, forms_by_participant):
        expense = self.get_expense()
        for form in forms_by_participant:
            participant, participant_expense_form = form

            participant_expense_form.participant = participant
            participant_expense_form.expense = expense
            participant_expense_form.save()

            update_total_amounts(self.get_event())

    def get(self, request, event_code, expense_id):
        forms_by_participant = self.create_forms()
        event = self.get_event()
        context = {'event':event,
                   'expense': self.get_expense(),
                   'forms_by_participant': forms_by_participant,}
        context['currency_unit'] = event.currencys.filter(is_active = True).first().title
        return render(request, 'expenses/split_payment.html', context = context)
    
    def post(self, request:HttpRequest , event_code, expense_id):
        forms_by_participant = self.create_forms(post_data=request.POST)
        context = {'event':self.get_event(),
                   'expense': self.get_expense(),
                   'forms_by_participant': forms_by_participant,}
        is_all_valid = self.is_all_forms_valid(forms_by_participant)
        if is_all_valid:
            self.save_all_forms(forms_by_participant)
            event = self.get_event()
            expense = self.get_expense()
            return redirect('split_payment_Success', event_code = event.code, expense_id = expense.id)

        return render(request, 'expenses/split_payment.html', context = context)

class SplitPaymentSuccessView(PaymentMixin, TemplateView):
    template_name = 'expenses/split_payment_success.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ExpensesListView(EventMemberRequiredMixin, ListView):
    template_name = 'expenses/expenses_list.html'
    model = models.Expenses
    context_object_name = 'expenses'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().filter(event = self.get_event()).order_by('-expense_date', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_event()
        context['currency_unit'] = event.currencys.filter(is_active = True).first().title
        return context

class EpensesDeleteView(PaymentMixin, View):
    @transaction.atomic
    def delet_expense(self):
        expense = self.get_expense()
        if expense.total_amount == 0:
            expense.delete()
    def post(self, request, event_code, expense_id):
        self.delet_expense()
        if request.POST.get('page_name') == 'expenses_list':
            return redirect('expenses_list', event_code = event_code)
        return redirect('dashboard', event_code = event_code)

class CurrencyHandlerView(EventMemberRequiredMixin, View):
    def post(self, request, event_code):
        event = self.get_event()
        currency_id = request.POST.get('remove')
        request_type = 'remove'
        if currency_id is None:
            currency_id = request.POST.get('active')
            request_type = 'active'
        if currency_id is not None and event.currencys.filter(id=currency_id).exists():
            currency = event.currencys.filter(id=currency_id).first()
            if request_type == 'remove' and currency.is_active is False:
                currency.delete()
            elif currency.is_active is False:
                for cur in event.currencys.all():
                    if cur == currency:
                        cur.is_active = True
                    else:
                        cur.is_active = False
                    cur.save()
        return redirect('dashboard', event_code = event_code)

class CurrencyUnitCreateView(EventMemberRequiredMixin, CreateView):
    form_class = forms.CurrencyUnitCreateForm
    template_name = 'expenses/currency_unit_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['event'] = self.get_event()
        return kwargs
    
    def get_success_url(self):
        event = self.get_event()
        return reverse_lazy('dashboard', kwargs = {'event_code': event.code})
