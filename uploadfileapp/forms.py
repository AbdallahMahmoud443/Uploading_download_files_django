
from django import forms
from uploadfileapp.models import Employee


class EmployeeForm(forms.ModelForm):
    pan_card_pic_blob = forms.ImageField(required=False)
    class Meta:
        model=Employee
        fields = '__all__'
        