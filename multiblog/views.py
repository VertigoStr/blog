from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, HttpResponse
from .forms import PublicationForm, CommentsAddForm, BloggerEditForm, BloggerAvatarLoadForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Blogger, BloggerManager, Publication, Comments
from django.contrib import auth
import datetime
import json


page_limit = 2 # ограничение на количество статей на странице

def pagination(response_data, paginator, page):

	try:
		pbl = paginator.page(page)
	except PageNotAnInteger:
		pbl = paginator.page(1)
	except EmptyPage:
		pbl = paginator.page(paginator.num_pages)

	for p in pbl:
		response_data.append({
			'result' : 'success',
			 'txt' : p.abstract, 
			 'post_title': p.title, 
			 'author' : p.author.get_full_name(),
			 'author_id' : p.author.id,
			 'post_id' : p.id,
			 'when' : p.time.strftime('%d.%m.%Y %H:%M')
		})
	return response_data
	

def main(request):
	publ = Publication.objects.all().order_by("-time")
	paginator = Paginator(publ, page_limit)

	if request.GET.get("page"):
		response_data = []
		response_data.append({"pages" : paginator.num_pages})
		page = int(request.GET.get("page"))
		response_data = pagination(response_data, paginator, page)
		return HttpResponse(json.dumps(response_data), content_type="application/json")	


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



	return render(request, 'multiblog/main.html', {'publ':paginator.page(1)})

def my_profile(request, pk):
	form = BloggerEditForm()
	if request.GET.get("post_id"):
		post_id = request.GET.get("post_id")
		Publication.objects.filter(id=post_id).delete()

	if request.POST:
		load_form = BloggerAvatarLoadForm(request.POST, request.FILES)
		if load_form.is_valid():
			blg = Blogger.objects.get(id=pk)
			ifile = request.FILES['avatar']
			blg.avatar.save(ifile.name, ifile)
			blg.save()

	if request.POST.get('edit'):
		new_name = request.POST.get('new_name')
		new_surname = request.POST.get('new_surname')
		new_phone = request.POST.get('new_phone')
		new_skype = request.POST.get('new_skype')


		blg = Blogger.objects.get(id=pk)
		blg.name = new_name if new_name else ""
		blg.surname = new_surname if new_surname else ""
		blg.phone = new_phone if new_phone else ""
		blg.skype = new_skype if new_skype else ""

		blg.save()
	
	
	load_form = BloggerAvatarLoadForm()

	publ = Publication.objects.all().order_by("-time").filter(author=pk)		
	blogger = Blogger.objects.get(id=pk)
	return render(request, 'multiblog/profile.html', {'blogger': blogger, 'publ':publ, 'form':form, 'load_form':load_form})	

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
			return HttpResponseRedirect("/publication/" + str(post.id))
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
