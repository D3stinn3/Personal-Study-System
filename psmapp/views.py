from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from psmapp.forms import SignupForm
from .forms import DocumentUploadForm, SubjectSuggestionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Document, Subject
from django.contrib.auth import logout


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # Load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('view_documents')  # Redirect to the documents page after signup
    else:
        form = SignupForm()
    return render(request, 'template/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('view_documents')  # Redirect to your documents view after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'template/login.html', {'form': form})

def logout_view(request):
    # Log out the user
    logout(request)
    
    # Optional: Add a message if you want to notify the user
    messages.success(request, "You have successfully logged out.")
    
    # Redirect to the login page (or any other page)
    return redirect('login')

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            return redirect('view_documents')
    else:
        form = DocumentUploadForm()
    return render(request, 'template/upload_document.html', {'form': form})

@login_required
def view_documents(request):
    documents = Document.objects.filter(user=request.user)
    
    for document in documents:
        document.is_pdf = document.file.name.lower().endswith('pdf')
        
    return render(request, 'template/view_documents.html', {'documents': documents})

@login_required
def recommend_subject(request):
    if request.method == 'POST':
        form = SubjectSuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.cleaned_data['suggestion']
            # Logic for handling new subject suggestion
            return redirect('document_list')
    else:
        form = SubjectSuggestionForm()
    return render(request, 'template/subject_recommendation.html', {'form': form})

@login_required
def document_list(request):
    user_documents = Document.objects.filter(user=request.user)
    subject_documents = Document.objects.filter(subject__in=[doc.subject for doc in user_documents])

    if request.method == 'POST':
        suggestion_form = SubjectSuggestionForm(request.POST)
        if suggestion_form.is_valid():
            suggestion = suggestion_form.save(commit=False)
            suggestion.user = request.user
            suggestion.save()
    else:
        suggestion_form = SubjectSuggestionForm()

    return render(request, 'template/document_list.html', {
        'documents': user_documents,
        'recommended_documents': subject_documents.exclude(user=request.user),
        'suggestion_form': suggestion_form,
    })