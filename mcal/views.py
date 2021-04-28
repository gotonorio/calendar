import datetime
import logging

import jpholiday
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from . import mixins
from .forms import ScheduleForm
from .models import Schedule


class MonthWithScheduleCalendar(mixins.MonthWithScheduleMixin, generic.TemplateView):
    """ 月間カレンダーを表示する """
    template_name = 'mcal/calendar_list.html'
    model = Schedule
    date_field = 'date'
    first_weekday = 6

    def set_holiday(self, cal):
        """ 日付行に休祭日をセットする """
        for w in cal:
            for d in w:
                if jpholiday.is_holiday(d):
                    holiday = '<span style="color:red; font-size:90%" >' + \
                        jpholiday.is_holiday_name(d) + '</span>'
                    w[d].insert(0, holiday)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        self.set_holiday(context['month_day_schedules'])
        return context


class CalendarCreateView(PermissionRequiredMixin, mixins.MonthCalendarMixin, generic.FormView):
    """ スケジュール登録画面 """
    template_name = 'mcal/calendar_form.html'
    model = Schedule
    date_field = 'date'
    form_class = ScheduleForm
    success_url = reverse_lazy('mcal:calendar')
    first_weekday = 6
    # 必要な権限
    permission_required = ("mcal.add_schedule")

    def get_datetime(self, year, month, day):
        if year and month and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        return date

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        date = self.get_datetime(year, month, day)
        try:
            text_align = Schedule.objects.values('align').get(date=date)['align']
        except Schedule.DoesNotExist:
            text_align = 'left'
        try:
            data = Schedule.objects.values('description').get(date=date)['description']
        except Schedule.DoesNotExist:
            data = ''
        try:
            memo = Schedule.objects.values('memo').get(date=date)['memo']
        except Schedule.DoesNotExist:
            memo = ''

        scheduleForm = ScheduleForm(initial={
            'align': text_align,
            'description': data,
            'memo': memo,
        })
        context['form'] = scheduleForm
        context['date'] = date
        return context

    def form_valid(self, form):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        date = self.get_datetime(year, month, day)
        schedule = form.save(commit=False)
        schedule.date = date
        Schedule.objects.update_or_create(
            date=date,
            defaults={
                'align': schedule.align,
                'description': schedule.description,
                'memo': schedule.memo,
                'date': date,
            }
        )
        return super().form_valid(schedule)


class CalendarMemo(generic.TemplateView):
    model = Schedule
    template_name = 'mcal/calendar_memo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        date = datetime.date(year=int(year), month=int(month), day=int(day))
        try:
            memo = Schedule.objects.values('memo').get(date=date)['memo']
        except Schedule.DoesNotExist:
            memo = ''
        context['date'] = date
        context['memo'] = memo
        return context


def search(request):
    """ 検索機能の処理 練習のため、関数viewで処理する。 """
    qs = Schedule.objects.order_by('-date').distinct()
    keyword = request.GET.get('keyword')
    if keyword:
        qs = qs.filter(Q(description__icontains=keyword) | Q(memo__icontains=keyword))
        messages.success(request, '「{}」の検索結果'.format(keyword))
    return render(request, 'mcal/search_result.html', {'search_result': qs})
