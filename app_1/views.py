from django.shortcuts import render, redirect, HttpResponse
from app_1.models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')



def register(request):
    errors = User.objects.register(request.POST)
    if len(errors) > 0:
        for key, error in errors.items():
            messages.error(request, error)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(email=request.POST['email'].lower(), password=pw_hash, first_name=request.POST['first_name'], last_name=request.POST['last_name'])
        request.session['user_id'] = user.id 
        messages.success(request, "Registered successfully")
        return redirect("/success")    



def login_process(request):
    errors = User.objects.login(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        return redirect("/")
    else:
        user = User.objects.filter(email=request.POST['email'].lower())
        if len(user) < 1:
            messages.error(request, "No User for that email")
            return redirect("/")
        
        if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
            print(f"LOG - Setting session value 'user_id' = {user[0].id}")
            request.session['user_id'] = user[0].id
            return redirect("/success")
        else:
            messages.error(request, "Incorrect Password!")
            return redirect("/")



def success(request):
    if 'user_id' not in request.session:
        messages.error(request, "Permission Denied")
        return redirect("/")

    user_id = request.session['user_id']

    context = {
        "user_id": request.session['user_id'],
        "user": User.objects.get(id=user_id), 
    }
    
    return render(request, 'success.html', context)



def logout(request):
    request.session.clear()
    messages.success(request, "You have successfully logged out")
    return redirect("/")