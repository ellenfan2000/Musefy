from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
from .gptutilize import *

def home(request):
    if request.method == 'POST':   
        form = Query(request.POST)
        if form.is_valid():
            
            # form_data = {
            #     "time": form.cleaned_data['Time'], 
            #     "date": form.cleaned_data['Date'], 
            #     "curatorial": form.cleaned_data['Curatorial'], 
            #     "start": form.cleaned_data['Start_time'],
            #     "end": form.cleaned_data['End_time'], 
            #     "artist": form.cleaned_data['Artist'],
            #     "theme":form.cleaned_data['Theme'], 
            #     "age": form.cleaned_data['Age']
            # }
            response = gen_message(form.cleaned_data['Time'], form.cleaned_data['Date'], form.cleaned_data['Curatorial'], 
                                   form.cleaned_data['Period'], form.cleaned_data['Artist'],
                                   form.cleaned_data['Theme'], form.cleaned_data['Age'])
            request.session['result'] = response

            return redirect("result_tour")
    else:
        print("not post")
        form = Query()
    return render(request = request, template_name = "homepage.html",context={"form":form})

'''
register a new user
'''

def result_tour(request):
    response = request.session.get('result')
    length = len(response)
    for i in range(length):
        response.append(response[i]['Related'][0])
    
    for art in response:
        art['OfficialLink'] = "https://en.wikipedia.org/wiki/"+  art['ArtPiece'].replace(" ", "_")
    
    return render(request = request, template_name = "result.html",context={"response":response})

# def register(request):
#     if request.user.is_authenticated:
#         messages.error(request, "You already are a user")
#         return redirect("/")
#     if request.method=="POST":
#         form=RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("/")
#     else:
#         form=RegisterForm()
#     return render(request, "register.html",{"form":form})
