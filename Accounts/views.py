# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from Accounts.forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
import base64
from django.core.files.base import ContentFile
import os.path
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.
def loginsignup(request):
	return render(request,'loginsignup.html',{})

def usernameProfile(request, username):
	try:
		profileUser = User.objects.get(username=username)
		return render(request,'usernameProfile.html',{'profileUser':profileUser})
	except:
		return render(request,'oops.html',{'message':'Username not found!'})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'account_activation_invalid.html', {})

def account_activation_sent(request):
	return render(request,'account_activation_sent.html',{})

def account_activation_invalid(request):
	return render(request,'account_activation_invalid.html',{})

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		errors = False
		input_values = {}
		input_values['username'] = request.POST.get('username')
		input_values['first_name'] = request.POST.get('first_name')
		input_values['last_name'] = request.POST.get('last_name')
		input_values['email'] = request.POST.get('email')
		input_values['mobile_number'] = request.POST.get('mobile_number')
		input_values['college_name'] = request.POST.get('college_name')

		if form.is_valid ():
			if form.cleaned_data.get('first_name')=="":
				form.errors['first_name'] = ['This field is required']
				errors = True
			if form.cleaned_data.get('last_name')=="":
				form.errors['last_name'] = ['This field is required']
				errors = True
			if form.cleaned_data.get('email')=="":
				form.errors['email'] = ['This field is required']
				errors = True
			if errors==True:
				return render(request, 'loginsignup.html', {'form': form, 'input_values':input_values})
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			user.refresh_from_db()  # load the profile instance created by the signal
			user.profile.mobile_number = form.cleaned_data.get('mobile_number')
			user.profile.college_name = form.cleaned_data.get('college_name')
			user.save()
			current_site = get_current_site(request)
			subject = 'Activate your MechMania account'
			message = render_to_string('account_activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			user.email_user(subject, message)
			return redirect('Accounts:account_activation_sent')
		else:
			if form.cleaned_data.get('first_name')=="":
				form.errors['first_name'] = ['This field is required']
			if form.cleaned_data.get('last_name')=="":
				form.errors['last_name'] = ['This field is required']
			if form.cleaned_data.get('email')=="":
				form.errors['email'] = ['This field is required']
			return render(request, 'loginsignup.html', {'form': form, 'input_values':input_values})
	else:
		form = SignUpForm()
	return render(request, 'loginsignup.html', {'form': form})

@login_required(login_url='/loginsignup.html')
def profile(request):
	return render(request,'profile.html',{})

@login_required(login_url='/loginsignup.html')
def change_profile_picture(request):
	if request.method == 'POST':
		try:
			data = request.POST.get('pic')

			if data=='':
				try:
					request.user.profile.profile_picture = None
					request.user.save()
					return HttpResponse('pass')
				except:
					return HttpResponse('fail')

			imgFormat, imgstr = data.split(';base64,')
			ext = imgFormat.split('/')[-1]

			data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

			imgfile = open(os.path.abspath(os.path.dirname(__name__))+'/static/profile_pics/'+request.user.username+'.'+ext, "wb")
			imgfile.write(base64.b64decode(imgstr))
			imgfile.close()
			request.user.profile.profile_picture = 'profile_pics/'+request.user.username+'.'+ext
			request.user.save()
			return HttpResponse('pass')
		except:
			return HttpResponse('fail')
	else:
		return render(request, 'profile.html', {})

@login_required(login_url='/loginsignup.html')
def updateProfile(request):
	if request.method == 'POST':
		try:
			firstname_v = request.POST.get('firstname')
			lastname_v = request.POST.get('lastname')
			birthdate_v = request.POST.get('birthdate')
			about_v = request.POST.get('about')
			mobile_number_v = request.POST.get('mobile_number')
			address_v = request.POST.get('address')
			collegename_v = request.POST.get('collegename')
			branch_v = request.POST.get('branch')
			gender_v = request.POST.get('gender')

			form = {}
			is_valid = True

			if len(firstname_v)>=30:
				is_valid = False
				form['firstname'] = 'Firstname too long'
			if len(lastname_v)>=150:
				is_valid = False
				form['lastname'] = 'Lastname too long'
			if birthdate_v!=' ' and birthdate_v!='' and birthdate_v!=None:
				try:
					birthdate = datetime.strptime(birthdate_v, '%d-%m-%Y')
					if datetime.now()<birthdate:
						is_valid = False
						form['birthdate'] = 'Invalid birthdate'
				except ValueError:
					is_valid = False
					form['birthdate'] = 'Invalid birthdate'
			if len(about_v)>=500:
				is_valid = False
				form['about'] = 'About too long'
			if len(mobile_number_v)!=10:
				is_valid = False
				form['mobile_number'] = 'Mobile number must have 10 digits'
			if len(address_v)>=500:
				is_valid = False
				form['address'] = 'Address too long'
			if len(collegename_v)>=100:
				is_valid = False
				form['college_name'] = 'College name too long'
			if len(branch_v)>=500:
				is_valid = False
				form['branch'] = 'Branch too long'
			if gender_v!='Male' and gender_v!='Female' and gender_v!='Other':
				is_valid = False
				form['gender'] = 'Invalid gender'

			if is_valid==False:
				form['pass'] = 'False'
				return JsonResponse(form)
			else:
				request.user.first_name = firstname_v
				request.user.last_name = lastname_v
				request.user.profile.about = about_v
				request.user.profile.mobile_number = mobile_number_v
				request.user.profile.address = address_v
				request.user.profile.college_name = collegename_v
				request.user.profile.branch = branch_v
				request.user.profile.gender = gender_v[0:1]
				if birthdate_v!=' ' and birthdate_v!='' and birthdate_v!=None:
					request.user.profile.birth_date = birthdate
				else:
					request.user.profile.birth_date = None
				request.user.save()
				form['pass'] = 'True'
				return JsonResponse(form)
		except:
			form['pass'] = 'False'
			return JsonResponse(form)
	else:
		return render(request, 'profile.html', {})
