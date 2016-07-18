from django import forms
from django.contrib import auth
from .models import Blogger, Publication, Comments

import datetime

class BloggerAuthForm(forms.ModelForm):

	class Meta:
		model = Blogger
		fields = ('email', 'password', )
		widgets = {
			'email' : forms.EmailInput(
				attrs = {
					'class':'form-control',
					'placeholder':'Email'
				}
			),

			'password' : forms.PasswordInput(
				attrs = {
					'class':'form-control',
					'placeholder':'Password'
				}
			),
		}

class PublicationForm(forms.ModelForm):
	

	class Meta:
		model = Publication
		fields = ('title', 'abstract', 'full_text',)
		widgets = {
			'title' : forms.TextInput(
				attrs = {
					'class':'form-control', 
					'placeholder':'Название', 
					'required':True
				}
			),

			'abstract': forms.Textarea(
				attrs={
					'class':'form-control',  
					'placeholder':'Краткое описание', 
					'rows':'6', 
					'required': True
				}
			),

			'full_text': forms.Textarea(
				attrs={
					'class':'form-control',  
					'placeholder':'Текст статьи (Доступны html-тэги)', 
					'rows':'12', 
					'required': 
					True
				}
			),
		}

class CommentsAddForm(forms.ModelForm):

	class Meta:
		model = Comments
		fields = ['text']
		widgets = {
			'text' : forms.TextInput(
				attrs={
					'id':'comment',
					'class':'form-control', 
					'placeholder':'Присоединиться к обсуждению'
				}
			)
		}


class BloggerEditForm(forms.ModelForm):

	class Meta:
		model = Blogger
		fields = ('name', 'surname', 'phone', 'skype', )
		widgets = {
			'name' : forms.TextInput(
				attrs={
					'class':'form-control', 
					'id':'name'
				}
			),

			'surname' : forms.TextInput(
				attrs={
					'class':'form-control', 
					'id':'surname'
				}
			),

			'phone' : forms.TextInput(
				attrs={
					'class':'form-control', 
					'id':'phone'
				}
			),

			'skype' : forms.TextInput(
				attrs={
					'class':'form-control', 
					'id':'skype'
				}
			),
		}

class BloggerAvatarLoadForm(forms.Form):
	avatar = forms.FileField()
