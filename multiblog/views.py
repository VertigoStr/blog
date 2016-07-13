from django.shortcuts import render, HttpResponseRedirect
from .forms import UserAuthForm
from .models import Blogger, BloggerManager
from django.contrib import auth

def main(request):
	form = UserAuthForm()
	if request.GET.get('logout'):
		auth.logout(request)
		return HttpResponseRedirect("")

	if request.method == "POST":
		email = request.POST['email']
		password = request.POST['password']

		if 'submit-register' in request.POST:
			print('submit-register')
			new_user = Blogger.objects.create_user(email, password)

		new_user = auth.authenticate(email=email, password=password)
		
		if new_user:
			auth.login(request, new_user)	

		return HttpResponseRedirect("/my_profile")		


	return render(request, 'multiblog/main.html', {'form':form, 'user': auth.get_user(request)})

def my_profile(request):
	return render(request, 'multiblog/profile.html', {'user': auth.get_user(request),})	