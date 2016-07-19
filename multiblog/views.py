from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.urlresolvers import reverse
from .forms import PublicationForm, CommentsAddForm
from .forms import BloggerEditForm, BloggerAvatarLoadForm, BloggerAuthForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Blogger, BloggerManager, Publication, Comments
from django.contrib import auth
from django.views.generic import View
from django.views.generic.edit import FormView, UpdateView

import datetime
import json

def rating(request):
	if request.GET.get('rating_value'):
		rating_value = int(request.GET.get('rating_value'))
		post_id = int(request.GET.get('post_id'))
		print(rating_value, post_id)
		publ = Publication.objects.get(id=post_id)
		publ.full_rating += rating_value
		publ.count_of_users += 1
		publ.save()

		res = int(publ.full_rating / publ.count_of_users)
		return HttpResponse(json.dumps({'res':res}), content_type="application/json")

def search(request):
	if request.GET.get("search_value"):
		search_value = request.GET.get("search_value")
		val = Publication.objects.filter(title=search_value)

		response_data = []
		for p in val:
			response_data.append({
				'result' : 'success',
			 	'txt' : p.abstract, 
			 	'post_title': p.title, 
			 	'author' : p.author.get_full_name(),
			 	'author_id' : p.author.id,
			 	'post_id' : p.id,
			 	'when' : p.time.strftime('%d.%m.%Y %H:%M')
			})

		return HttpResponse(json.dumps(response_data), content_type="application/json")


def delete(request):
	if request.GET.get("post_id"):
		post_id = request.GET.get("post_id")
		Publication.objects.filter(id=post_id).delete()
		return HttpResponse(request.path)

def edit(request, pk):
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
	return HttpResponse(request.path)	

class MainPageAuth(FormView):
	form_class = BloggerAuthForm
	template_name = 'multiblog/main.html'	

	error = ''
	page_limit = 2 # ограничение на количество статей на странице
	user_id = -1
	publ = Publication.objects.all().order_by("-time")
	paginator = Paginator(publ, page_limit)

	def pagination(self, paginator, page):
		response_data = []
		response_data.append({"pages" : paginator.num_pages})
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

	def context(self):
		return {
			'publ' : self.paginator.page(1),
		    'form' : self.form_class,
			'error' : self.error
		}


	def get(self, request):
		if request.GET.get("page"):
			page = int(request.GET.get("page"))
			response_data = self.pagination(self.paginator, page)
			return HttpResponse(json.dumps(response_data), content_type="application/json")
		else:
			return render(request, self.template_name, self.context())

	def get_success_url(self):
		return reverse("my_profile", kwargs={'pk': self.user_id})

	def register(self, request):
		email = request.POST['email']
		password = request.POST['password']		

		try:
			user = Blogger.objects.create_user(email, password)
			return self.auth(request)
		except Exception:
			self.error = 'Данный Email-адрес уже используется'
			return render(request, self.template_name, self.context())

	def auth(self, request):
		email = request.POST['email']
		password = request.POST['password']
		user = auth.authenticate(email=email, password=password)

		if user:
			self.user_id = user.id
			auth.login(self.request, user)
			return super(MainPageAuth, self).form_valid(self.get_form())
		else:
			self.error = 'Неверный логин или пароль'
			return render(request, self.template_name, self.context())

	def post(self, request, *args, **kwargs):
		form = self.get_form()

		if 'submit-register' in request.POST:
			return self.register(request)

		if 'submit-log-in' in request.POST:
			return self.auth(request)

class MyProfile(FormView):
	template_name = 'multiblog/profile.html'
	form_class = BloggerAvatarLoadForm

	def get_context_data(self, **kwargs):
		pk = self.kwargs['pk']
		return {
			'publ' : Publication.objects.all().order_by("-time").filter(author=pk),
			'blogger' : Blogger.objects.get(id=pk),
			'form' : BloggerEditForm(),
			'load_form' : self.form_class	
		}

	def get_success_url(self):
		return reverse("my_profile", kwargs={'pk': self.request.user.id})

	def form_valid(self, form):
		blg = Blogger.objects.get(id=self.request.user.id)
		ifile = self.request.FILES['avatar']
		blg.avatar.save(ifile.name, ifile)
		blg.save()
		return super(MyProfile, self).form_valid(form)

class NewPublication(FormView):
	template_name = 'multiblog/new.html'
	form_class = PublicationForm

	publ_id = -1

	def get_success_url(self):
		return reverse("full", kwargs={'pk': self.publ_id})

	def form_valid(self, form):
		form.instance.time = datetime.datetime.now()
		form.instance.author = self.request.user
		form.save()
		
		self.publ_id = form.instance.id
		return super(NewPublication, self).form_valid(form)

class EditPublication(UpdateView):
	template_name = 'multiblog/new.html'
	model = Publication
	form_class = PublicationForm

	def get_context_data(self, **kwargs):
		post = get_object_or_404(Publication, pk=self.kwargs['pk'])
		form = PublicationForm(instance=post)
		return {'form' : form, 'mode' : True}

	def get_success_url(self):
		return reverse("full", kwargs={'pk': self.kwargs['pk']})


	def form_valid(self, form):
		form.instance.time = datetime.datetime.now()
		form.instance.author = self.request.user
		form.save()
		return super(EditPublication, self).form_valid(form)

class FullPublication(FormView):
	template_name = 'multiblog/full.html'
	form_class = CommentsAddForm

	def get_context_data(self, **kwargs):
		pk=self.kwargs['pk']
		post = get_object_or_404(Publication, pk=pk)
		count = post.count_of_users if post.count_of_users > 0 else 1
		res = int(post.full_rating / count)
		return {
			'post' : post,
			'comments' : Comments.objects.filter(publication=pk).order_by('-time'),
			'form' : self.form_class,
			'rating' : res,
		}

	def post(self, request, *args, **kwargs):
		comment_text = request.POST.get('comment')

		comment = Comments(
			text=comment_text, 
			author=auth.get_user(request), 
			time=datetime.datetime.now(), 
			publication=get_object_or_404(Publication, pk=kwargs['pk'])
		)
		comment.save()

		response_data = {
			'result' : 'success',
			'txt' : comment_text,
			'author' : comment.author.get_full_name(),
			'avatar' : comment.author.avatar.url,
			'author_id' : comment.author.id,
			'when' : comment.time.strftime('%d.%m.%Y %H:%M')

		}

		return HttpResponse(json.dumps(response_data), content_type="application/json")		