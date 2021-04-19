from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
import random

from influxdb import InfluxDBClient


db_client = InfluxDBClient(host='127.0.0.1', port="8086")

db_client.switch_database('fence_project_db')

result = db_client.query('select last("Voltage") from "Fence_project"')
voltage = list(result.get_points())[0]['last']

result = db_client.query('select last("Current") from "Fence_project"')
current = list(result.get_points())[0]['last']




# Create your views here.
def register(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.fence_id = form.cleaned_data.get('fence_id')
            user.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        form=UserRegisterForm()
    return render(request,'users/register.html', {'form':form})
@login_required
def profile(request):
    # combining the edit view with the profile
    return render(request, 'users/profile.html')

@login_required()
def edit(request):
    if request.method=='POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Update successfull! ')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context= {'u_form': u_form, 'p_form': p_form}
    return render(request, 'users/edit.html',context)

@login_required()
def dashboard(request):
    context={'voltage': voltage,'current':current}
    return render(request,'users/dashboard.html', context)