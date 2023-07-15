from django.forms import ModelForm, TextInput
from django import forms
from vehiculo.models import VehiculosModel

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class VehiculoForm(ModelForm):

    class Meta:
        model = VehiculosModel
        fields = '__all__'
        widgets = {
            'precio': TextInput(attrs={'type': 'number'})
        }




class RegisterUserForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user