from django.urls import path
from . import views

app_name = 'mcal'

urlpatterns = [
    path('', views.MonthWithScheduleCalendar.as_view(), name='calendar'),
    path('calendar/', views.MonthWithScheduleCalendar.as_view(), name='calendar'),
    path('calendar/<int:year>/<int:month>/',
         views.MonthWithScheduleCalendar.as_view(), name='calendar'),
    path('create/', views.CalendarCreateView.as_view(), name='create'),
    path('create/<int:year>/<int:month>/', views.CalendarCreateView.as_view(), name='create'),
    path('create/<int:year>/<int:month>/<int:day>/', views.CalendarCreateView.as_view(), name='create'),
    path('memo/<int:year>/<int:month>/<int:day>/', views.CalendarMemo.as_view(), name='memo'),
    path('search/', views.search, name='search'),
]
