from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SymptomForm(forms.Form):
    SYMPTOM_CHOICES = [
        ('fever', 'Fièvre'),
        ('cough', 'Toux'),
        ('headache', 'Mal de tête'),
        ('fatigue', 'Fatigue'),
        ('sore_throat', 'Mal de gorge'),
        ('shortness_of_breath', 'Essoufflement'),
        ('chest_pain', 'Douleur thoracique'),
        ('nausea', 'Nausée'),
        ('vomiting', 'Vomissements'),
        ('diarrhea', 'Diarrhée'),
    ]
    
    symptoms = forms.MultipleChoiceField(
        choices=SYMPTOM_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'symptom-checkbox'}),
        required=True,
        label='Sélectionnez vos symptômes'
    )

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='البريد الإلكتروني')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'اسم المستخدم',
            'password1': 'كلمة المرور',
            'password2': 'تأكيد كلمة المرور',
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='اسم المستخدم')
    password = forms.CharField(label='كلمة المرور', widget=forms.PasswordInput)