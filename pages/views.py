from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')

def wallet_view(request):
    return render(request, 'wallet.html')

def profile_view(request):
    return render(request, 'profile.html')

def search_view(request):
    return render(request, 'search.html')

def movies_view(request):
    return render(request, 'movies.html')

def login_view(request):
    return render(request, 'login.html')

def register_view(request):
    return render(request, 'register.html')

def otp_verify_view(request):
    return render(request, 'otp_verify.html')

def forgot_password_view(request):
    return render(request, 'forgot_password.html')

def new_password_view(request):
    return render(request, 'new_password.html')

def comments_view(request):
    return render(request, 'comments.html')

def movies_view(request):
    return render(request, 'movies.html')