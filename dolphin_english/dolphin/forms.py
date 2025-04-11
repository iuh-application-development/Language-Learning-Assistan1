from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Topic, Section, SubTopic, AudioExercise
from django import forms
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    nickname = forms.CharField(max_length=255)

    def save(self, request):
        user = super().save(request)
        user.nickname = self.cleaned_data['nickname']
        user.save()
        return user
    
class CustomeUserCreationForm(UserCreationForm):
    nickname = forms.CharField(label='Nickname', widget=forms.TextInput(attrs={'placeholder':"Nickname"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Enter Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':"Confirm Password"}))
    class Meta:
        model = User
        fields = ["nickname", "email", "password1", "password2"]

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'placeholder': "Email",
            'class': 'form-control',
        })
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': "Enter Password",
            'class': 'form-control',
        })
    )

class ChangeNickName(forms.Form):
    nickname = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'placeholder':'Enter new nickname',
        'class':'form-control'
    }))


class ChangeEmail(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':"Email", 'class':'form-control'}))

class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password', 'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password', 'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        pw = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')

        if pw and confirm and pw != confirm:
            raise forms.ValidationError('Passwords do not match.')

        return cleaned_data


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = '__all__'  # Bao gồm tất cả các trường của Topic model
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter topic name'}),
            'slug': forms.TextInput(attrs={'placeholder': 'Enter slug for the topic'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter section title', 'class': 'form-control'}),
            'topic': forms.Select(attrs={'class': 'form-control'}),
        }

class SubTopicForm(forms.ModelForm):
    class Meta:
        model = SubTopic
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter subtopic title', 'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'full_textkey': forms.Textarea(attrs={'placeholder': 'Enter full text key', 'class': 'form-control'}),
            'full_audioSrc': forms.URLInput(attrs={'placeholder': 'Enter audio URL', 'class': 'form-control'}),
        }


class AudioExerciseForm(forms.ModelForm):
    class Meta:
        model = AudioExercise
        fields = '__all__' 
        widgets = {
            'subtopic': forms.Select(attrs={'class': 'form-control'}),
            'audioSrc': forms.URLInput(attrs={'placeholder': 'Enter audio URL', 'class': 'form-control'}),
            'correct_text': forms.Textarea(attrs={'placeholder': 'Enter correct text', 'class': 'form-control'}),
            'position': forms.NumberInput(attrs={'placeholder': 'Enter exercise position', 'class': 'form-control'}),
        }
    
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'nickname', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'last_login', 'last_active_date'
        ]
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(),
            'is_staff': forms.CheckboxInput(),
            'last_login': forms.DateTimeInput(attrs={'readonly': 'readonly'}),
            'last_active_date': forms.DateInput(attrs={'type': 'date'})
        }
