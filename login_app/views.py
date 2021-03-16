from django.shortcuts import HttpResponse, render, redirect
from django.contrib import messages
from .models import User
import bcrypt   #for password encryption/decryption
from time import gmtime, strftime
from datetime import datetime, date
from dateutil.relativedelta import *
from dateutil.parser import *
import pytz

def index(request):
    if 'logout' in request.session:
        del request.session['logout']
        context = {
            'logout' : 'A log out has occurred. Please, Login or Register to continue.'
        }
    else:
        context = {}
    return render(request, 'login_registration.html', context)

def user_login(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST, user_status='old')
        if len(errors) == 0:
            user = User.objects.filter(email_address=request.POST['email_address_login'])
            request.session['user_id'] = user[0].id
            return redirect(f'/user/login/success/{request.session["user_id"]}')
        else:
            for key, value in errors.items():
                messages.error(request, value)
            thefields = {
                'email_address_login' : request.POST['email_address_login']
            }
            context = {'user': thefields}
    else:
        context = {}
    return render(request, 'login_registration.html', context)

def user_login_success(request, user_id=0):
    if request.method == "GET":
        if 'user_id' in request.session:
            if user_id == int(request.session['user_id']):
                context = {
                    'user' : User.objects.get(id=user_id)
                }
                return render(request, 'login_success.html', context)
            return redirect('/user/logout')
    return redirect('/')

def user_logout(request):
    request.session.flush()
    request.session['logout'] = 'Yes'
    return redirect('/')

def user_registration(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST, user_status='new')

        if len(errors) == 0:
            create_result = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                birth_date = request.POST['birth_date'],
                email_address = request.POST['email_address'],
                password = bcrypt.hashpw(request.POST['password1'].encode(), bcrypt.gensalt()).decode()
            )
            request.session['user_id'] = create_result.id
            return redirect(f'/user/login/success/{request.session["user_id"]}')
        else:
            for key, value in errors.items():
                messages.error(request, value)
            thefields = {
                'first_name' : request.POST['first_name'],
                'last_name' : request.POST['last_name'],
                'birth_date' : request.POST['birth_date'],
                'email_address' : request.POST['email_address']
            }
            context = {'user': thefields}
    else:
        context = {}
    return render(request, 'login_registration.html', context)