from django.urls import path
from . import views

app_name = 'mcal'

urlpatterns = [
    path('', views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'),
    path('month_with_schedule/', views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'),
    path('month_with_schedule/<int:year>/<int:month>/', views.MonthWithScheduleCalendar.as_view(), name='month_with_schedule'),
    path('mycalendar/', views.MyCalendar.as_view(), name='mycalendar'),
    path('mycalendar/<int:year>/<int:month>/<int:day>/', views.MyCalendar.as_view(), name='mycalendar'),
]
