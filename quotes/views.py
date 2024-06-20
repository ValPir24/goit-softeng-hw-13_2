from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .forms import AuthorForm, QuoteForm
from .models import Author, Quote

User = get_user_model()

def home(request):
    return render(request, 'quotes/home.html')

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Author added successfully!')
            return redirect('home')
    else:
        form = AuthorForm()
    return render(request, 'quotes/add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quote added successfully!')
            return redirect('home')
    else:
        form = QuoteForm()
    return render(request, 'quotes/add_quote.html', {'form': form})

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'quotes/author_detail.html', {'author': author})

def all_quotes(request):
    quotes = Quote.objects.all()
    return render(request, 'quotes/all_quotes.html', {'quotes': quotes})

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password reset email has been sent.')
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'registration/password_reset_form.html', {'form': form})

def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    return render(request, 'registration/password_reset_confirm.html')

def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html')


