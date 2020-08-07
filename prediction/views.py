from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError

from .utils import predict
from .forms import DocumentForm

import json, os, pickle

supported_extension = [".txt", ".md"] 
template_name="prediction/home.html"
context = {"models":["Bag of word", "TD-IDF", 
            #"BERT"
            ], 
            "defaut_model":"TD-IDF", "message": ""}

def home(request):
    context.update({"at_home":True, "succes": False, "form" : DocumentForm})  
    context["message"] = ""
    return render(request, template_name, context)

def about(request):
    return render(request, "prediction/about.html", {"at_about":True})

@csrf_exempt
def prediction(request):
    context["form"] = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try :
                docfile = request.FILES['docfile']
                if is_supported(file_name = str(docfile)) :
                    content = get_content(docfile)
                    context["content"] = content
                else :
                    context.update({"succes": False})
                    context["message"] = 'File type not supported.'
                    return TemplateResponse(request, template_name, context)
                    
            except MultiValueDictKeyError :
                content =  request.POST["eula"]
                context["content"] = content
                if not content :
                    context["message"] = 'Please fill in the text box or choose a file.'
                    return TemplateResponse(request, template_name, context)

            model_name = request.POST["model_name"]
            output = predict(model_name = model_name, eula = content)
            context.update({"succes": True,"output": output})
            context["message"] = ""
            return TemplateResponse(request, template_name, context)
    else :
        return home(request)        
   
def get_content(document):
    content = document.read().decode('utf-8')
    print(content)
    return content

def is_supported(file_name):
    _, extension = os.path.splitext(file_name) # file_name.split(".")[-1]
    if extension in supported_extension :
        return True
    else :
        return False
        
def handle_uploaded_file(filestream, destination_path):
    #destination_path = settings.MEDIA_ROOT + destination_path
    with open(destination_path, 'wb+') as destination_file:
        for chunk in filestream.chunks():
            destination_file.write(chunk)