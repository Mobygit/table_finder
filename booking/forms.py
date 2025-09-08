from django import forms
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'mobile', 'email', 'num_guests', 'date', 'time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'num_guests': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'min': date.today().isoformat(),
                'max': (date.today() + timedelta(days=30)).isoformat(),
                'class': 'form-control'
            }),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def clean_date(self):
        selected_date = self.cleaned_data['date']
        today = date.today()
        max_date = today + timedelta(days=30)

        if selected_date < today:
            raise ValidationError("You cannot select a past date.")
        elif selected_date > max_date:
            raise ValidationError("Reservations can only be made for the next 30 days.")
        return selected_date
