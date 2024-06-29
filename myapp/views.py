from multiprocessing import context
import os
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Student
from .forms import StudentRegistration

# Create your views here.
def HomePage(request):
    return render (request,'home.html')
def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        print(uname,email,pass1,pass2)

        if pass1!=pass2:
             return HttpResponse("Your password and confirm password are not same!!")
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
        
    return render(request, 'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else: 
            return HttpResponse("Username or password is incorrect!!")
    return render(request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def add_show(request):
    if request.method == 'POST':
        form = StudentRegistration(request.POST, request.FILES)
        print('success',form)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentRegistration()
    
    # students = Student.objects.all()
    return render(request, 'addshow.html', {'form': form})

def showformdata(request):
    fm = StudentRegistration()
    return render(request,'addshow.html',{'form':fm})

def index_show(request):
    return render(request,'index.html')

def detail(request):
    stud = Student.objects.all()

    context= {
        'stud':stud,
    }
    return render(request,'details.html',context)

# def edit(request,rollno):
#     print(rollno,'rollno')
#     stud = Student.objects.get(rollno=rollno)
#     print(stud,'sut')
#     # context= {
#     #     'stud':stud,
#     # }
#     return redirect(request,'details.html',context)

def delete(request,rollno):
    print(rollno,'rollno')
    s=Student.objects.get(rollno=rollno)
    print(s,'student')
    s.delete()
    return redirect('detail')

# def add_show(request):
#     if request.method == 'POST':
#         form = StudentRegistration(request.POST, request.FILES)
#         print('success',form)
#         if form.is_valid():
#             form.save()
#             return redirect('student_list')  # Redirect to a list of students or another appropriate page
#     else:
#         form = StudentRegistration()
#     return render(request, 'addshow.html', {'form': form})

def edit (self, request):
    return render(request,'editstud.html')