from datetime import date
from django import forms    
from .models import Product, Availability, Reservation

class ReservationForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            # Check if the start_date is before the end_date
            if start_date >= end_date:
                raise forms.ValidationError("Start date must be before the end date.")

            # Check if the selected dates are in the future
            today = date.today()
            if start_date < today or end_date < today:
                raise forms.ValidationError("Selected dates must be in the future.")

            # Check availability for the selected dates
            product = self.data.get("product_id")
            availabilities = Availability.objects.filter(
                product=product,
                date__range=[start_date, end_date]
            )
            if not availabilities.exists():
                raise forms.ValidationError("Selected dates are not available for this product.")
