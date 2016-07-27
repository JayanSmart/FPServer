from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'Hello, world. You\'re at the polls index.', {}  )