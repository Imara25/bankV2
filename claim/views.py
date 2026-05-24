from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'claim/index.html')
def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request,'claim/register.html',{'error':'username already taken'})
            if User.objects.filter(email=email).exists():
                return render(request,'claim/register.html',{'error':'Email already exist'})
            user=User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            return redirect('login')
    else:
        return render(request,'claim/register.html')
def login_view(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            return render(request,'claim/login.html',{'error':'invalid credentials'})       
    return render(request, 'claim/login.html')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'claim/dashboard.html',{'user':request.user})
