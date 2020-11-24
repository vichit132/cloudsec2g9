import calendar

from datetime import datetime, date, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User,auth
from django.db.models import Q
from django.core.mail import send_mail

from .models import *
from .utils import Calendar
from .forms import EventForm, SearchForm

@login_required(login_url='signup')
def index(request):
    return HttpResponse('hello')

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = 'signup'
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month, self.request.user)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

@login_required(login_url='signup')
def create_event(request):    
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        date = str(start_time).split(' ')[0].split('-')
        time = str(start_time).split(' ')[1].split(':')
        dateformat = date[2]+'/'+date[1]+'/'+date[0]+' '+time[0]+':'+time[1]
        enddate = str(end_time).split(' ')[0].split('-')
        endtime = str(end_time).split(' ')[1].split(':')
        enddateformat = enddate[2]+'/'+enddate[1]+'/'+enddate[0]+' '+endtime[0]+':'+endtime[1]
        
        send_mail(
            title,
            dateformat+' To '+enddateformat+'\nDetail:'+description,
            'MyToDoListSec2@gmail.com',
            [request.user.email],
        )
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        return HttpResponseRedirect(reverse('calendarapp:calendar'))
    return render(request, 'event.html', {'form': form})

class EventEdit(generic.UpdateView):
    model = Event
    fields = ['title', 'description', 'start_time', 'end_time']
    template_name = 'event.html'

@login_required(login_url='signup')
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    context = {
        'event': event
    }
    return render(request, 'event-details.html', context)

def todolist (request):
    data=Event.objects.filter(user=request.user).order_by('start_time')
    
    return render (request, 'todolist.html',{'posts':data})

def search(request):
    if request.method=='POST':
        kw = request.POST.get('name','')
        form = SearchForm(request.POST, initial={'title':kw})
    else:
        kw = request.GET.get('name','')
        form = SearchForm(initial={'title':kw})

    data=Event.objects.filter(Q(title=kw)|Q(description=kw))[:10]

    return render(request, 'search.html',{'form':form,'data':data})


def Event_Delete(request, id):
        Event.objects.get(id=id).delete()
                
        return redirect('/')