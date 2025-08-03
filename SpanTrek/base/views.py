from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from .forms import My_User_Creation_Form

def home_page(request):
    # If user is not authenticated, redirect to login page
    if not request.user.is_authenticated:
        return redirect('login_page')
    
    return render(request, 'home.html')


def login_page(request):
    page = 'login'
    # If user is already logged in, redirect to home page from login page
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        error_message = False
        print(email, password)
        
        try:
            user = User.objects.get(email=email)
        except:
            error_message = True
            messages.error(request, 'Password or email is incorrect')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home_page')
        else:
            if not error_message:
                messages.error(request, 'Password or email is incorrect')

    context = {'page': page}
    return render(request, 'login_register.html', context)

def register_page(request):
    page = 'register'
    form = My_User_Creation_Form()
        
    if request.method == 'POST':
        form = My_User_Creation_Form(request.POST)
        if form.is_valid():
            # Commit=false -> not saving to database yet, firstly clearing up data and logging up on the page
            user = form.save(commit=False)
            # user.username = user.username
            user.save()
            login(request, user)
            return redirect('home_page')
        else:
            messages.error(request, 'Coś poszło nie tak. Spróbuj ponownie')

    context = {'register_form': form, 'page': page}
    return render(request, 'login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('login_page')
