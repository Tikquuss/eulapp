from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError

import json, os, pickle
import PyPDF2
import fitz
import docx
import randomcolor
from threading import Thread

from .forms import DocumentForm, supported_extension 
from . import AppScope
from .utils_eulascripts import text_is_valid, pyMuPDF_clauses_extraction

def app_scope(request):
    """
    This class allows to load all models at the beginning of the application, 
    and these models have an application scope (i.e. they are available during the whole life of the application).
    see prediction.__init__.AppScope class
    """
    app = AppScope()
    app_thead = Thread(target = app.start_app_scope)
    app_thead.start()
    return redirect('home')

def home(request):
    """Home page"""
    from . import ai_modeles
    context = {
        "at_home" : True, 
        "succes": False, 
        "form" : DocumentForm,
        "message" : "",
        "models" : ai_modeles
    }
    return render(request, "prediction/index.html", context)

def about(request):
    """About view"""
    return render(request, "prediction/about.html", {"at_about":True})

def prediction_interface(request):
    from . import ai_modeles
    context = {
        "at_prediction" : True, 
        "succes": False, 
        "form" : DocumentForm,
        "message" : "",
        "models" : ai_modeles
    }
    return render(request, "prediction/prediction.html", context)

@csrf_exempt
def prediction(request):
    """Prediction view"""

    context = {}
    from . import ai_modeles
    context["models"] = ai_modeles
    context["succes"]= False
    context["at_prediction"] = True
    context["from_text_area"] = False
    context["coloration"] = False
    
    doc_type, clauses = None, None

    if request.method == 'POST':    

        form = DocumentForm(request.POST, request.FILES)
        
        if form.is_valid():
            try :

                # From file

                docfile = request.FILES['docfile']
                
                if is_supported(file_name = str(docfile)) :
                    content, doc_type, clauses, join = get_content(docfile)
                    context["content"] = join.join(content)

                    if not text_is_valid(text = context["content"]) :
                        context["message"] = 'Invalid file content'
                        return JsonResponse(context)
            
                else :
                    context["message"] = 'File type not supported.'
                    return JsonResponse(context)

            except MultiValueDictKeyError :
                
                # From text area
                content =  request.POST["eula"]
    
                if not text_is_valid(text = content) :
                    context["message"] = 'Please fill in the text box or choose a file.'
                    return JsonResponse(context)
                else :
                    context["content"] = content
                    content = [content]
                    context["from_text_area"] = True

            try :
                model_name = request.POST["model_name"]
            except MultiValueDictKeyError :
                context["message"] = 'Choose a model.'
                return JsonResponse(context)
            
            try :
                coloration = request.POST["coloration"]
            except MultiValueDictKeyError:
                coloration = False
            context["coloration"] = coloration

            try :
                from . import methods_dic 

                if not clauses :
                    clauses = convert_to_clauses(content, context["from_text_area"], doc_type)

                clause_list = list(clauses.values())
                response = methods_dic[model_name](eula = clause_list)

                context["html"] = []
                
                for _, clause, output, meta_data in zip(list(clauses.keys()), clause_list, response["output"], response["meta_data"]) :
                    if text_is_valid(text = clause) :
                        try :  
                            context["html"].append((
                                output,
                                parse_to_html(text = clause, meta_data = meta_data, with_coloration = coloration) 
                            ))
                            
                        except AssertionError :
                            context["html"].append((output, clause))
                    else :
                        context["html"].append((output, ""))
                        
            except KeyError:
                output = ["No model name %s"%model_name]

            context["succes"] = True
            context["output"] = output
            context["message"] = ""
            
            return JsonResponse(context)
    else :
        return home(request)        

def convert_to_clauses(content : list, from_text_area : bool = False, doc_type : str = None):

    if doc_type in [".doc", ".docx"] :
        return {i : clause for i, clause in enumerate(content)}
    elif doc_type == ".pdf" :
        return

    a = " ".join(content).strip()
    if from_text_area :
        b = a.split("\r\n\r\n")
    else :
        b = a.split("\n\n")
        
    return {i : clause for i, clause in enumerate(b)}



def get_content(document):

    _, extension = os.path.splitext(str(document))
    clauses = None
    join = " "

    if extension == ".pdf" :
        """
        pdfReader = PyPDF2.PdfFileReader(document)
        content = [pdfReader.getPage(page).extractText() for page in range(pdfReader.numPages)]
        content = [text for text in content if text_is_valid(text = text)]
        """
        destination_path = os.path.join("prediction", str(document))
        handle_uploaded_file(filestream = document, destination_path = destination_path)
        clauses = pyMuPDF_clauses_extraction(destination_path)
        content = list(clauses.values())
        os.remove(destination_path)

    elif extension in [".doc", ".docx"] :
        doc = docx.Document(document)
        content = doc.paragraphs
        content = [para.text for para in content if text_is_valid(text = para.text)]
        clauses = {i : clause for i, clause in enumerate(content)}
        
        
    else :
        content = document.read().decode('utf-8')
        content = content if text_is_valid(text = content) else ""
        join = "\n\n"
        content = content.split(join)
        
        clauses = {i : clause for i, clause in enumerate(content)}

    return content, extension, clauses, join

def is_supported(file_name : str):
    _, extension = os.path.splitext(file_name) 
    if extension in supported_extension :
        return True
    else :
        return False

def parse_to_html(text, meta_data, with_coloration = False):

    if with_coloration :
        text_set = list(set(text.split()))
        text_set = [word for word in text_set if word in meta_data.keys()]
        collection = {}
        for word in text_set :
            freq = meta_data.get(word, 0)
            try :
                collection[freq].append(word)
            except KeyError :
                collection[freq] = [word]

        _, color_list = get_color_list(n_element = len(collection.keys()), color_list = ["red", "blue", "orange"])

        # No coloring of texts of zero frequency
        collection[0] = []
        
        html_dico = {}
        
        for index, word_list in enumerate(list(collection.values())) :
            for word in word_list :
                try :
                    html_dico[word]
                except :
                    color = color_list[index].replace("'", "")
                    word_tmp = word.replace("<", "").replace(">", "") # to avoid bad template parsing
                    html_dico[word] = "<span style='background-color : " + color +" !important'>" + word_tmp + "</span>"
                
        text = " ".join(html_dico.get(word, word) for word in text.split())

    text = text.replace("\n", "<br />")

    return text 

def get_color_list(n_element : int,
                        color_list : list = ["red", "blue", "orange", "yellow", "green", "indigo", "purple",  "teal", "cyan"]):
    rand_color = randomcolor.RandomColor()
    assert n_element != 0
    assert color_list
    color_list = color_list[:n_element]
    n_class = len(color_list) 
    n_element_per_class = n_element // n_class
    a = {
        color : rand_color.generate(hue = color, count = n_element_per_class)
        for color in color_list
    } 
    for i in range(n_element % n_class) :
    	color =  color_list[i]
    	a[color] = a[color] + rand_color.generate(hue = color, count = 1)

    b = []
    for value in a.values():
        b += value

    return a, b

def handle_uploaded_file(filestream, destination_path : str):
    #destination_path = settings.MEDIA_ROOT + destination_path
    with open(destination_path, 'wb+') as destination_file:
        for chunk in filestream.chunks():
            destination_file.write(chunk)

    return destination_path

"""
import random 
import matplotlib.pyplot as plt 

def generate_colors(n : int): 
    rgb_values = [] 
    hex_values = [] 
    r = int(random.random() * 256) 
    g = int(random.random() * 256) 
    b = int(random.random() * 256) 
    step = 256 / n  
    for _ in range(n): 
        r += step 
        g += step 
        b += step 
        r = int(r) % 256 
        g = int(g) % 256 
        b = int(b) % 256 
        r_hex = hex(r)[2:] 
        g_hex = hex(g)[2:] 
        b_hex = hex(b)[2:] 

        hex_values.append('#' + r_hex + g_hex + b_hex) 
        rgb_values.append((r,g,b)) 

    return rgb_values, hex_values 
"""