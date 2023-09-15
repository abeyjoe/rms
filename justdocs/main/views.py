from django.shortcuts import render

# Create your views here.
def homepage(request):

    return render(request, "home/index.html", {})

def template_handler(request):
    return render(request, "home/documentpage.html", {})

def template_view(request):
    return render(request, "home/template-html",{})