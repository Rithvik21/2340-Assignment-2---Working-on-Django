from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomErrorList

@login_required
def logout(request):
    auth_logout(request)
    return redirect('index')

def login(request):
    template_data = {'title': 'Login'}
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '')
    user = authenticate(request, username=username, password=password)
    if user is None:
        template_data['error'] = 'The username or password is incorrect.'
        return render(request, 'accounts/login.html', {'template_data': template_data})
    auth_login(request, user)
    return redirect('index')

def signup(request):
    template_data = {'title': 'Sign Up'}
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})
    form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
    if form.is_valid():
        form.save()
        return redirect('login')
    template_data['form'] = form
    return render(request, 'accounts/signup.html', {'template_data': template_data})

@login_required
def orders(request):
    template_data = {'title': 'Orders', 'orders': request.user.order_set.all()}
    return render(request, 'accounts/orders.html', {'template_data': template_data})
