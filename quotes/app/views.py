from django.shortcuts import render,redirect, get_object_or_404
from .models import Quote
from django.contrib.auth.decorators import login_required,  user_passes_test
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def is_admin(user):
    return user.is_superuser

@login_required(login_url='login')
def dashboard(request):
    if request.user.is_superuser:
        return redirect('admin')
    return redirect('index')

@login_required(login_url='login')
def index(request):
    quote_of_the_day = Quote.objects.order_by('?').first()
    context = {
        'quote_of_the_day': quote_of_the_day,
        'all_quotes': Quote.objects.all()
    }
    return render(request, 'index.html', context)

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required(login_url='login')
def signout(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import Quote
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import user_passes_test

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def admin(request):
    quotes = Quote.objects.all()
    return render(request, 'admin.html', {'quotes': quotes})

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def add(request):
    if request.method == 'POST':
        text = request.POST['text']
        author = request.POST['author']
        quote = Quote.objects.create(text=text, author=author)
        return JsonResponse({'id': quote.id, 'text': quote.text, 'author': quote.author}, status=201)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def edit(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    if request.method == 'POST':
        quote.text = request.POST['text']
        quote.author = request.POST['author']
        quote.save()
        return JsonResponse({'id': quote.id, 'text': quote.text, 'author': quote.author}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def delete(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id)
    quote.delete()
    return JsonResponse({'id': quote_id}, status=200)
