from django import forms
from .models import Blogger, Publication

class UserAuthForm(forms.ModelForm):

	class Meta:
		model = Blogger
		fields = ('email', 'password',)
		widgets = {
			'email': forms.EmailInput(attrs={'class':'form-control',  'placeholder':'Ваш почтовый адрес', 'required': True}),
			'password': forms.TextInput(attrs={'class':'form-control',  'placeholder':'Пароль', 'required': True}),
		}

class PublicationForm(forms.ModelForm):

	class Meta:
		model = Publication
		fields = ('title', 'abstract', 'full_text', )
		widgets = {
			'title' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Название', 'required':True}),
			'abstract': forms.Textarea(attrs={'class':'form-control',  'placeholder':'Краткое описание', 'rows':'6', 'required': True}),
			'full_text': forms.Textarea(attrs={'class':'form-control',  'placeholder':'Текст статьи', 'rows':'12', 'required': True}),
		}