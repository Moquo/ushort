from django.shortcuts import render
from django.http import HttpResponse

# Index page
def index(request):
    return render(request, "shortener/index.html", {})