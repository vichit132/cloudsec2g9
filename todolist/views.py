from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from calendarapp.forms import SignupForm
from django.core.mail import send_mail
import random
import string

def signup(request):
    forms = SignupForm()
    if request.method == 'POST':
        forms = SignupForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('calendarapp:calendar')
            else :
                messages.info(request,'Username หรือ Password ไม่ถูกต้อง')
    context = {'form': forms}
    
    return render(request, 'signup.html', context)


def user_logout(request):
    logout(request)
    return redirect('signup')

def forgetpassword (request):
    if request.method == 'POST':
        print(request.POST['email'])
        try:     
            checkemail=User.objects.get(email=request.POST['email'])
            letters = string.ascii_lowercase+string.ascii_uppercase+'0123456789'
            result_str = ''.join(random.choice(letters) for i in range(8))
            checkemail.set_password(result_str)
            checkemail.save()
            print(result_str)
            send_mail(
            'ลืมรหัสผ่าน',
            'รหัสผ่านของคุณถูกเปลี่ยนเป็น'+' '+result_str,
            'MyToDoListSec2@gmail.com',
            [checkemail.email],
            )
            messages.info(request,'password ใหม่ได้ถูกส่งไปยัง email แล้ว')
            return redirect('/')
             
        except User.DoesNotExist:     
            checkemail = None
            messages.info(request,'ไม่พบ email นี้')
        
    return render (request, 'forgetpassword.html')
    


def calendar (request):
    return render (request, 'calendar.html')


def todolist (request):
    return render (request, 'todolist.html')


def createForm (request):
    return render (request, 'register.html')


def loginForm (request):
    return render (request, 'signup.html')


def register (request):
    return render (request, 'register.html')


def addUser (request):
    username=request.POST['username']
    firstname=request.POST['firstname']
    lastname=request.POST['lastname']
    email=request.POST['email']
    password=request.POST['password']
    repassword=request.POST['repassword']

    if password ==repassword :
        if User.objects.filter(username=username).exists():
            messages.info(request, 'UserName นี้มีคนใช้แล้ว')
            return redirect('/createForm')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email นี้มีคนใช้แล้ว')
            return redirect('/createForm')
        else :
            user=User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=firstname,
            last_name=lastname
            )
            user.save()
            return redirect('/')
    else :
        messages.info(request, 'รหัสผ่านไม่ตรงกัน')
        return redirect('/createForm')

def newpassword (request):
    password=request.POST['password']
    repassword=request.POST['repassword']
    if password ==repassword :
        try:
            checkemail2=User.objects.get(email=request.POST['email'])
            checkemail2.set_password(password)
            checkemail2.save()
            send_mail(
            'เปลี่ยนรหัสผ่าน',
            'รหัสผ่านของคุณถูกเปลี่ยนเป็น'+' '+password,
            'MyToDoListSec2@gmail.com',
            [checkemail2.email],
            )
            messages.info(request,'password ของคุณถูกเปลี่ยนเรียบร้อย')
            return redirect('calendarapp:calendar')
        except  User.DoesNotExist:     
                checkemail2 = None
                messages.info(request,'ไม่พบ email นี้')
                return redirect('/changepassword')
    else :
            messages.info(request, 'รหัสผ่านไม่ตรงกัน')
            return redirect('/changepassword')

def changepassword (request):
    return render (request, 'changepassword.html')