import datetime
import logging

#from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from . import mixins
from .forms import ScheduleForm
from .models import Schedule


class MonthWithScheduleCalendar(mixins.MonthWithScheduleMixin, generic.TemplateView):
    """ 月間カレンダーを表示する """
    template_name = 'mcal/calendar.html'
    model = Schedule
    date_field = 'date'
    first_weekday = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class CalendarCreateView(mixins.MonthCalendarMixin, generic.FormView):
    """ スケジュール登録画面 """
    template_name = 'mcal/calendar_form.html'
    model = Schedule
    date_field = 'date'
    form_class = ScheduleForm
    success_url = reverse_lazy('mcal:calendar')

    def get_datetime(self, year, month, day):
        if year and month and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        return date

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        date = self.get_datetime(year, month, day)
        try:
            data = Schedule.objects.values('description').get(date=date)['description']
        except Schedule.DoesNotExist:
            data = ''

        scheduleForm = ScheduleForm(initial={
            'description': data
        })
        month_calendar_context = self.get_month_calendar()
        context.update(month_calendar_context)
        context['form'] = scheduleForm
        context['date'] = date
        logging.debug(date)
        return context

    def form_valid(self, form):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        date = self.get_datetime(year, month, day)
        schedule = form.save(commit=False)
        schedule.date = date
        logging.debug(schedule.date)
        logging.debug(schedule.description)
        Schedule.objects.update_or_create(
            date=date,
            defaults={
                'description': schedule.description,
                'date': date,
            }
        )
        return super().form_valid(schedule)
