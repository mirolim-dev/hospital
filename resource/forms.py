from django import forms
from .models import BatchMedicine

class BatchMedicineAdminForm(forms.ModelForm):
    class Meta:
        model = BatchMedicine
        fields = [
            'medicine', 
            'amount', 
            'measure', 
            'available_till'
        ]