from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event
from django.db.models import Q

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None, user=None):
		self.year = year
		self.month = month
		self.user = user
		super(Calendar, self).__init__()
	


	# formats a day as a td
	# filter events by day

	def formatday(self, day, events):		
		xxx = datetime(self.year,self.month,(1 if day == 0 else day))
		events_per_day = events.filter(start_time__date__lte=xxx,end_time__date__gte=xxx, user=self.user)
		d = ''		
		for event in events_per_day:
			if event.id%9==0:
				tcor='Tometo'
			elif event.id%8==0:
				tcor='Orange'
			elif event.id%7==0:
				tcor='DodgerBlue'
			elif event.id%6==0:
				tcor='MediumSeaGreen'
			elif event.id%5==0:
				tcor='SlateBlue'
			elif event.id%4==0:
				tcor='LawnGreen'
			elif event.id%3==0:
				tcor='Red'
			elif event.id%2==0:
				tcor='DarkTurquoise'				
			else:
				tcor='Violet'			
			d += f'<div style="background-color:DarkTurquoise; width:103%; position:relative;background-color:{tcor}">{event.get_html_url} </div>'
		
		if day != 0:
			return f"<td><span class='date'>{day}</span><ul style='width:100%; margin-left:-5px;'> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(start_time__year=self.year, start_time__month__lte=self.month)
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal