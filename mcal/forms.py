from django import forms
from .models import Schedule


class ScheduleForm(forms.ModelForm):
    """ bulmaに対応するためのModelForm """

    class Meta:
        model = Schedule
        fields = ('align', 'description', 'memo')
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'textarea',
                'rows': '3',
            }),
            'align': forms.Select(attrs={
                'class': 'select',
            }),
            'memo': forms.Textarea(attrs={
                'class': 'textarea',
                'rows': '3',
            }),
        }

    def __init__(self, *args, **kwargs):
        """ classはここで設定するのが楽。checkboxはcssで変更は不可能みたい """
        super().__init__(*args, **kwargs)
        self.fields['align'].widget.attrs["class"] = "select-css"
