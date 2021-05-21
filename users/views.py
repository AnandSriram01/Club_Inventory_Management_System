from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


def index(request):
	return render(request,'users/index.html')


@login_required
def special(request):
	return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))


def register(request):
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileInfoForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			profile.name = user.first_name
			# if 'profile_pic' in request.FILES:
			#     print('found it')
			#     profile.profile_pic = request.FILES['profile_pic']
			profile.save()
			registered = True
		else:
			print(user_form.errors)
	else:
		user_form = UserForm()
		profile_form = UserProfileInfoForm()
	return render(request,'users/registration.html',
						  {'user_form':user_form,
						   'profile_form':profile_form,
						   'registered':registered})


def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request,user)
				return HttpResponse('Welcome', username)
			else:
				return HttpResponse("Your account was inactive.")
		else:
			print("Someone tried to login and failed.")
			print("They used username: {} and password: {}".format(username,password))
			return HttpResponse("Invalid login details given")
	else:
		return render(request, 'users/login.html', {})


def member_dashboard(request, uname):
	member = UserProfile.objects.get(name=uname)
	requests = member.request_set.all()
	return render(request, 'users/member.html', {'requests':requests})


@login_required
def createRequest(request):
	created = False
	if request.method == 'POST':
		request_form = RequestInfoForm(data=request.POST)
		if request_form.is_valid():
			request_form.save()
			created = True
		else:
			print(request_form.errors)
	else:
		request_form = RequestInfoForm()

	return render(request,'users/requestForm.html', {'request_form':request_form, 'created':created})


@login_required
def createClub(request):
	created = False
	if request.method == 'POST':
		club_form = ClubInfoForm(data=request.POST)
		if club_form.is_valid():
			club_form.save()
			created = True
		else:
			print(club_form.errors)
	else:
		club_form = ClubInfoForm()

	return render(request,'users/clubForm.html', {'club_form':club_form, 'created':created})


@login_required
def createItem(request):
	created = False
	if request.method == 'POST':
		item_form = ItemInfoForm(data=request.POST)
		if item_form.is_valid():
			item_form.save()
			created = True
		else:
			print(item_form.errors)
	else:
		item_form = ItemInfoForm()

	return render(request,'users/itemForm.html', {'item_form':item_form, 'created':created})


def updateReqStatus(request, pk):
	updated = False
	req = Request.objects.get(id=pk)

	if request.method == 'POST':
		request_form = RequestInfoForm(request.POST, instance=req)
		if request_form.is_valid():
			request_form.save()
			updated = True
	else:
		request_form = RequestInfoForm(instance=req)

	context = {'request_form':request_form, 'updated':updated}
	return render(request, 'users/requestForm.html', context)


def deleteUser(request, pk):
	deleted = False
	user = UserProfile.objects.get(id=pk)

	if request.method == "POST":
		user.delete()
		deleted = True

	context = {'user':user, 'deleted':deleted}
	return render(request, 'users/deleteUser.html', context)
