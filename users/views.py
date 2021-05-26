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
			profile.name = user.first_name + ' ' + user.last_name
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
				return redirect('member_db')
			else:
				return HttpResponse("Your account was inactive.")
		else:
			print("Someone tried to login and failed.")
			print("They used username: {} and password: {}".format(username,password))
			return HttpResponse("Invalid login details given")
	else:
		return render(request, 'users/login.html', {})


@login_required
def createRequest(request, member):
	created = False
	memberProfile = UserProfile.objects.get(pk=member)
	if request.method == 'POST':
		request_form = RequestInfoForm(data=request.POST, initial={'member':memberProfile, 'status':'Awaiting Approval'})
		request_form.fields['item'].queryset = memberProfile.club.items_of_club.all()
		request_form.fields['member'].disabled = True
		request_form.fields['status'].disabled = True
		if request_form.is_valid():
			req = request_form
			req.member = member
			req.save()
			created = True
			return redirect('member_db')
		else:
			print(request_form.errors)
	else:
		request_form = RequestInfoForm(initial={'member':memberProfile, 'status':'Awaiting Approval'})
		request_form.fields['item'].queryset = memberProfile.club.items_of_club.all()
		request_form.fields['member'].disabled = True
		request_form.fields['status'].disabled = True

	return render(request,'users/requestForm.html', {'request_form':request_form, 'created':created})


@login_required
def createClub(request):
	created = False
	if request.method == 'POST':
		club_form = ClubInfoForm(data=request.POST)
		if club_form.is_valid():
			club_form.save()
			created = True
			return redirect('admin_db')
		else:
			print(club_form.errors)
	else:
		club_form = ClubInfoForm()

	return render(request,'users/clubForm.html', {'club_form':club_form, 'created':created})


@login_required
def createItem(request, club):
	created = False
	clubProfile = Club.objects.get(id=club)
	print(clubProfile.name)
	if request.method == 'POST':
		item_form = ItemInfoForm(data=request.POST, initial={'club':clubProfile})
		item_form.fields['club'].disabled = True
		if item_form.is_valid():
			item = item_form
			item.club = club
			item.save()
			return redirect('convenor_db')
			created = True
		else:
			print(item_form.errors)
	else:
		item_form = ItemInfoForm(initial={'club':clubProfile})
		item_form.fields['club'].disabled = True
		print(item_form.fields)
		# item_form.fields['user_club'] = clubProfile.name

	return render(request,'users/itemForm.html', {'item_form':item_form, 'created':created})


def updateReqStatus(request, req):
	updated = False
	req = Request.objects.get(id=req)

	if request.method == 'POST':
		request_form = RequestInfoForm(request.POST, instance=req)
		request_form.fields['comment'].disabled = True
		request_form.fields['member'].disabled = True
		request_form.fields['item'].disabled = True
		if request_form.is_valid():
			request_form.save()
			updated = True
			return redirect('convenor_db')
	else:
		request_form = RequestInfoForm(instance=req)
		request_form.fields['comment'].disabled = True
		request_form.fields['member'].disabled = True
		request_form.fields['item'].disabled = True
		print(request_form)

	context = {'request_form':request_form, 'updated':updated}
	return render(request, 'users/requestForm.html', context)


def deleteUser(request, user):
	deleted = False
	user = UserProfile.objects.get(id=user)

	if request.method == "POST":
		user.delete()
		deleted = True
		return redirect('admin_db')

	context = {'user':user, 'deleted':deleted}
	return render(request, 'users/deleteUser.html', context)


def admin_db(request):
	print(request.user.userprofile)
	reqs = Request.objects.all()
	users = UserProfile.objects.all()
	items = Item.objects.all()
	clubs = Club.objects.all()

	context = {'reqs':reqs, 'users':users, 'items':items, 'clubs':clubs}

	return render(request, 'users/admin_dashboard.html', context)


def member_db(request):
	print(request.user.username)
	userobj = request.user
	memberProfile = UserProfile.objects.get(user = userobj)
	clubProfile = memberProfile.club
	print(memberProfile)
	reqs = memberProfile.requests_of_user.all
	items = clubProfile.items_of_club.all

	context = {'memberProfile':memberProfile, 'reqs':reqs, 'items':items}
	print(context)

	return render(request, 'users/member_dashboard.html', context)


def convenor_db(request):
	print(request.user.username)
	userobj = request.user
	memberProfile = UserProfile.objects.get(user = userobj)
	clubProfile = memberProfile.club
	print(memberProfile)
	reqs = Request.objects.filter(item__club = clubProfile)
	items = clubProfile.items_of_club.all
	users = UserProfile.objects.filter(club=clubProfile)

	context = {'memberProfile':memberProfile, 'reqs':reqs, 'items':items, 'users':users}
	print(context)

	return render(request, 'users/convenor_dashboard.html', context)
