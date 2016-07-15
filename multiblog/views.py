from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from .forms import PublicationForm, CommentsAddForm
from .models import Blogger, BloggerManager, Publication, Comments
from django.contrib import auth
import datetime
import json

def main(request):
	publ = Publication.objects.all().order_by("-time")
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
			try:
				new_user = Blogger.objects.create_user(email, password)
			except Exception:
				error = 'Данный Email-адрес уже используется'
				return render(request, 'multiblog/main.html', {'publ':publ, 'error': error})

		new_user = auth.authenticate(email=email, password=password)

		if new_user:
			auth.login(request, new_user)	
			return HttpResponseRedirect("/my_profile/" + str(auth.get_user(request).id))
		else:
			return render(request, 'multiblog/main.html', {'publ':publ, 'error': error})

	return render(request, 'multiblog/main.html', {'publ':publ})

def my_profile(request, pk):

	if request.method == "GET":
		if request.GET.get("post_id"):
			post_id = request.GET.get("post_id")
			Publication.objects.filter(id=post_id).delete()

	blogger = Blogger.objects.get(id=pk)
	publ = Publication.objects.all().order_by("-time").filter(author=pk)
	return render(request, 'multiblog/profile.html', {'blogger': blogger, 'publ':publ})	

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

	return render(request, 'multiblog/new.html', {'form':form, 'mode':False})		

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
	return render(request, 'multiblog/new.html', {'form':form, 'mode':True})

def full_publication(request, pk):
	form = CommentsAddForm()
	post = get_object_or_404(Publication, pk=pk)
	comments = Comments.objects.filter(publication=pk).order_by('-time')

	if request.method == "POST":
		comment_text = request.POST.get('comment')
		response_data = {}
		if comment_text:
			comment = Comments(text=comment_text, author=auth.get_user(request), time=datetime.datetime.now(), publication=post)
			comment.save()

			response_data['result'] = 'success'
			response_data['txt'] = comment.text
			response_data['author'] = comment.author.get_full_name()
			response_data['avatar'] = comment.author.avatar.url
			response_data['author_id'] = comment.author.id
			response_data['when'] = comment.time.strftime('%d.%m.%Y %H:%M')

			return HttpResponse(json.dumps(response_data), content_type="application/json")


	return render(request, 'multiblog/full.html', {'post':post, 'comments':comments, 'form':form})
