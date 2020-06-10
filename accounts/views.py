from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from contacts.models import Contact


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "Welcome back!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    if request.method == 'GET':
        return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Passwords must match.")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already taken")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, first_name=first_name, password=password,
                                        last_name=last_name)

        auth.login(request, user)
        messages.success(request, 'Welcome!')
        return redirect('/')

    if request.method == 'GET':
        return render(request, 'accounts/register.html')


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        "contacts": user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "Logged out")
        return redirect('index')
