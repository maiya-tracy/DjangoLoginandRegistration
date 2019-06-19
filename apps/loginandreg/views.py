from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import bcrypt
import datetime
import re


# ------
# ROUTES
# ------

def index(request):
    return render(request, 'loginandreg/index.html')

def addUserToDB(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        messages.error(request, request.POST["first_name"], "holdFName")
        messages.error(request, request.POST["last_name"], "holdLName")
        messages.error(request, request.POST["email"], "holdEmail")
        return redirect('/')
    else:
        DBfirst_name = request.POST["first_name"]
        DBlast_name = request.POST["last_name"]
        DBemail = request.POST["email"]
        pw_to_hash = request.POST["password"]
        DBpassword = bcrypt.hashpw(pw_to_hash.encode(), bcrypt.gensalt())
        DBpassword = DBpassword.decode()
        new_user = User.objects.create(DBfirst_name=DBfirst_name, DBlast_name=DBlast_name, DBemail=DBemail, DBpassword=DBpassword)
        request.session['userid'] = new_user.id
        request.session['first_name'] = new_user.DBfirst_name
        request.session['isloggedin'] = True
        request.session.modified = True
        return redirect("/success")

def loginUserToDB(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        messages.error(request, request.POST["emailLogin"], "holdLoginEmail")
        return redirect('/')
    else:
        current_user = User.objects.get(DBemail = request.POST['emailLogin'])
        request.session['userid'] = current_user.id
        request.session['isloggedin'] = True
        request.session['first_name'] = current_user.DBfirst_name
        return redirect("/success")

def success(request):
    if not request.session['isloggedin']:
        return redirect("/")
    return render(request, 'loginandreg/success.html')

def logout(request):
    request.session.clear()
    request.session['isloggedin'] = False
    return redirect('/')
