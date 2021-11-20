from django.shortcuts import render

def home(request):
    """Home page"""
    context = { "at_prediction" : False, "at_home":True}
    return render(request, "prediction/index.html", context)

def about(request):
    """About view"""
    return render(request, "prediction/about.html", {"at_about":True})

