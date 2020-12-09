from django import forms
from .models import Schedule


class ScheduleForm(forms.ModelForm):
    """ bulmaに対応するためのModelForm """

    class Meta:
        model = Schedule
        fields = ('description', 'align', 'memo')
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'textarea ',
                'rows': '5',
            }),
        }
