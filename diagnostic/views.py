from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SymptomForm, RegisterForm, LoginForm
from .models import DiagnosticHistory
from .ml.process import predict_disease

def register(request):
    if request.user.is_authenticated:
        return redirect('diagnostic:index')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'تم إنشاء الحساب بنجاح!')
            return redirect('diagnostic:index')
    else:
        form = RegisterForm()
    return render(request, 'diagnostic/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('diagnostic:index')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'مرحباً {username}!')
                return redirect('diagnostic:index')
    else:
        form = LoginForm()
    return render(request, 'diagnostic/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح!')
    return redirect('diagnostic:login')

@login_required(login_url='diagnostic:login')
def index(request):
    form = SymptomForm()
    return render(request, 'diagnostic/index.html', {'form': form})

@login_required(login_url='diagnostic:login')
def predict(request):
    if request.method == 'POST':
        form = SymptomForm(request.POST)
        if form.is_valid():
            symptoms = form.cleaned_data['symptoms']
            
            try:
                predictions = predict_disease(symptoms)
                
                if predictions:
                    top_disease = predictions[0]
                    DiagnosticHistory.objects.create(
                        user=request.user,  # ربط التشخيص بالمستخدم
                        symptoms=', '.join(symptoms),
                        predicted_disease=top_disease['disease'],
                        confidence=top_disease['probability']
                    )
                
                return render(request, 'diagnostic/result.html', {
                    'predictions': predictions,
                    'symptoms': symptoms
                })
            except Exception as e:
                messages.error(request, f"Erreur lors de la prédiction: {str(e)}")
                return redirect('diagnostic:index')
    
    return redirect('diagnostic:index')

@login_required(login_url='diagnostic:login')
def history(request):
    histories = DiagnosticHistory.objects.filter(user=request.user)[:20]  # فقط تشخيصات المستخدم
    return render(request, 'diagnostic/history.html', {'histories': histories})