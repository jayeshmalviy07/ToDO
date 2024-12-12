from django.shortcuts import render,redirect
from django.contrib.auth.models import User 
from todolist import models
from todolist.models import TODOO
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
 
def signup(request):
    if request.method=='POST':
        fnm=request.POST.get('fnm')
        emailid=request.POST.get('email')
        password=request.POST.get('pwd')
        print(fnm,emailid,password)
        my_user=User.objects.create_user(fnm,emailid,password)
        my_user.save()
        return redirect('/login')    
    return render(request,'signup.html') 

def auth_login(request):
    if request.method == 'POST':
        fnm=request.POST.get('fnm')
        pwd=request.POST.get('pwd')
        print(fnm,pwd)
        user1=authenticate(request,username=fnm,password=pwd)
        if user1 is not None:
            login(request,user1)
            return redirect('/todopage')
        else:
            return redirect('/login')
    return render(request, 'login.html')

@login_required(login_url='/login')
def todo(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        print(title)
        obj=models.TODOO(title=title,user=request.user)
        obj.save()
        user=request.user        
        res=models.TODOO.objects.filter(user=user).order_by('-date')
        return redirect('/todopage',{'res':res})
    res=models.TODOO.objects.filter(user=request.user).order_by('-date')
    return render(request, 'todo.html',{'res':res,})

@login_required(login_url='/login')
def edit_todo(request,srno):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj = models.TODOO.objects.get(srno=srno)
        obj.title = title
        obj.save()
        return redirect('/todopage')
    obj = models.TODOO.objects.get(srno=srno)
    return render(request, 'edit_todo.html', {'obj': obj})

@login_required(login_url='/login')
def delete_todo(request,srno):
    obj=models.TODOO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')

def signout(request):
    logout(request)
    return redirect('/login')