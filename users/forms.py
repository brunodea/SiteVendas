from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignupForm(forms.Form):
    name = forms.CharField(max_length=30, required=False, initial='Seu Nome', label='Nome')
    cpf  = forms.IntegerField(required=True, initial='', label='CPF')

    def __unicode__(self):
        return 'Signup Form'

class UserCreationFormExtended(UserCreationForm): 
    def __init__(self, *args, **kwargs): 
        super(UserCreationFormExtended, self).__init__(*args, **kwargs) 
        self.fields['first_name'].required = True 
        self.fields['last_name'].required = True 
        self.fields['email'].required = True

    class Meta: 
        model = User 
        fields = ('username', 'email', 'first_name', 'last_name') 
