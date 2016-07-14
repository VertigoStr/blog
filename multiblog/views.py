from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from .forms import UserAuthForm, PublicationForm
from .models import Blogger, BloggerManager, Publication
from django.contrib import auth
import datetime

def main(request):
	if request.GET.get('new'):
		return HttpResponseRedirect("/new/")

	if request.GET.get('logout'):
		auth.logout(request)
		return HttpResponseRedirect(request.path)

	if request.method == "POST":
		error = 'Неверный логин или пароль'
		email = request.POST['email']
		password = request.POST['password']

		if 'submit-register' in request.POST:
			print('submit-register')
			try:
				new_user = Blogger.objects.create_user(email, password)
			except Exception:
				error = 'Данный Email-адрес уже используется'

		new_user = auth.authenticate(email=email, password=password)

		if new_user:
			auth.login(request, new_user)	
			return HttpResponseRedirect("/my_profile/" + str(auth.get_user(request).id))
		else:
			return {'error': error}

	publ = Publication.objects.all().order_by("id")

	return render(request, 'multiblog/main.html', {'user': auth.get_user(request), 'publ':publ})

def my_profile(request, pk):
	blogger = Blogger.objects.get(id=pk)
	publ = Publication.objects.all().order_by("id").filter(author=pk)
	return render(request, 'multiblog/profile.html', {'blogger': blogger, 'publ':publ, 'user': auth.get_user(request),})	

def new_publication(request):

	if request.method == "POST":
		form = PublicationForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.title =  form.cleaned_data['title']
			post.abstract = form.cleaned_data['abstract']
			post.full_text =  form.cleaned_data['full_text']
			post.time = datetime.datetime.now()
			post.author = auth.get_user(request)
			post.save()
			return HttpResponseRedirect('/')
	else:
		form = PublicationForm()

	return render(request, 'multiblog/new.html', {'form':form, 'user': auth.get_user(request),})		

def edit_publication(request, pk):
	post = get_object_or_404(Publication, pk=pk)

	if request.method == "POST":
		form = PublicationForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.title =  form.cleaned_data['title']
			post.abstract = form.cleaned_data['abstract']
			post.full_text =  form.cleaned_data['full_text']
			post.time = datetime.datetime.now()
			post.author = auth.get_user(request)
			post.save()
			return HttpResponseRedirect("/publication/" + str(pk))
	else:
		form = PublicationForm(instance=post)
	return render(request, 'multiblog/new.html', {'form':form})

def full_publication(request, pk):
	post = get_object_or_404(Publication, pk=pk)
	return render(request, 'multiblog/full.html', {'user': auth.get_user(request), 'post':post})
