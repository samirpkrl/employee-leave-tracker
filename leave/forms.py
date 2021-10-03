from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Empleave

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2','is_superuser']

class DateInput(forms.DateInput):
    input_type = 'date'

class LeaveForm(forms.ModelForm):
    reason = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control','rows':'4','cols':'40' }
    ),required = True)
    title = forms.CharField(widget=forms.TextInput  (
        attrs={
            'class': 'form-control' }
    ),required = True)
    class Meta:
        model = Empleave
        fields = ('title','from_date','to_date','reason')
        labels = { 
            'title':'Add leave title',
            'from_date':'Select start date of leave',
            'to_date':'Select to date'
        }
        widgets = {
            'from_date': DateInput(),
            'to_date': DateInput(),
        }