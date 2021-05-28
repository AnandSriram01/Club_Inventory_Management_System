from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, Permission
from .models import *
from .forms import *
from .decorators import *


@login_required(login_url='users:user_login')
def user_logout(request):
	logout(request)
	return render(request, 'users/login.html')


@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['Admin'])
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
			# print(profile.role)

			role = profile.role
			group = Group.objects.get(name=role)
			user.groups.add(group)
			user.save()
			profile.save()

			registered = True

		else:
			print(user_form.errors)

	else:
		user_form = UserForm()
		profile_form = UserProfileInfoForm()
		print(profile_form)

	return render(request,'users/registration.html',
						  {'user_form':user_form,
						   'profile_form':profile_form,
						   'registered':registered})


def user_login(request):
	invalid = False

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request,user)
				role = request.user.groups.all()[0].name
				print(role)

				if role == 'Convenor':
					return redirect('convenor_db')
				elif role == 'Member':
					return redirect('member_db')
				elif role == 'Admin':
					return redirect('admin_db')

			else:
				return HttpResponse("Your account was inactive.")

		else:
			invalid = True
			return render(request, 'users/login.html', {'invalid':invalid})

	else:
		return render(request, 'users/login.html', {})


@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['Member'])
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


@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['Admin'])
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


@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['Convenor'])
def createItem(request, club):
	created = False
	clubProfile = Club.objects.get(id=club)

	# print(clubProfile.name)
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
		# print(item_form.fields)
		# item_form.fields['user_club'] = clubProfile.name

	return render(request,'users/itemForm.html', {'item_form':item_form, 'created':created})


@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['Convenor'])
def acceptRequest(request, req):
	requestobj = Request.objects.get(id=req)
	# print(requestobj.status)
	requestobj.status = 'Accepted By Convenor'
	requestobj.item.quantity -= 1

	requestobj.save()
	requestobj.item.save()
	# print(requestobj.status)

	return redirect('convenor_db')


@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['Convenor'])
def denyRequest(request, req):
	requestobj = Request.objects.get(id=req)
	# print(requestobj.status)
	requestobj.status = 'Rejected By Convenor'
	requestobj.save()
	# print(requestobj.status)

	return redirect('convenor_db')


@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['Admin'])
def deleteUser(request, user):
	deleted = False

	userprofile = UserProfile.objects.get(id=user)
	userobj = userprofile.user

	if request.method == "POST":
		userprofile.delete()
		userobj.delete()
		deleted = True

		return redirect('admin_db')

	context = {'user':user, 'deleted':deleted}
	return render(request, 'users/deleteUser.html', context)


@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['Admin'])
def admin_db(request):
	# print(request.user.userprofile)
	reqs = Request.objects.all()
	users = UserProfile.objects.filter(role__in=['Convenor','Member'])
	items = Item.objects.all()
	clubs = Club.objects.all()

	context = {'reqs':reqs, 'users':users, 'items':items, 'clubs':clubs}

	return render(request, 'users/admin_dashboard.html', context)


@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['Member'])
def member_db(request):
	# print(request.user.username)
	userobj = request.user

	memberProfile = UserProfile.objects.get(user = userobj)
	clubProfile = memberProfile.club
	# print(memberProfile)
	reqs = memberProfile.requests_of_user.all
	items = clubProfile.items_of_club.all

	context = {'memberProfile':memberProfile, 'reqs':reqs, 'items':items}
	# print(context)

	return render(request, 'users/member_dashboard.html', context)


@login_required(login_url='users:user_login')
@allowed_users(allowed_roles=['Convenor'])
def convenor_db(request):
	# print(request.user.username)
	userobj = request.user

	memberProfile = UserProfile.objects.get(user = userobj)
	clubProfile = memberProfile.club
	# print(memberProfile)
	reqs = Request.objects.filter(item__club = clubProfile)
	items = clubProfile.items_of_club.all()
	users = UserProfile.objects.filter(club=clubProfile, role='Member')
	# print(items)
	items_for_alert = []

	for item in items:
		item_qty = item.quantity
		item_reqs = item.requests_of_item.all()
		num_of_reqs = item_reqs.count()
		# print(item, item_qty, item_reqs, num_of_reqs)
		if num_of_reqs > item_qty:
			items_for_alert.append(item.name)

	context = {'memberProfile':memberProfile, 'reqs':reqs, 'items':items, 'users':users, 'items_for_alert':items_for_alert,}
	# print(context)

	return render(request, 'users/convenor_dashboard.html', context)
