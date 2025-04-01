from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import TextInput, PasswordInput

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(help_text="A valid email address, please.", required=True)
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
class LoginUserForm(forms.Form):

    username = forms.CharField(max_length=255,widget=TextInput(attrs={'class': 'form-control', 'placeholder':'Username'}))
    password = forms.CharField(max_length=255,widget=PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}))
    