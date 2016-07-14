from django import forms
from .models import Blogger, Publication, Comments

class PublicationForm(forms.ModelForm):

	class Meta:
		model = Publication
		fields = ('title', 'abstract', 'full_text', )
		widgets = {
			'title' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Название', 'required':True}),
			'abstract': forms.Textarea(attrs={'class':'form-control',  'placeholder':'Краткое описание', 'rows':'6', 'required': True}),
			'full_text': forms.Textarea(attrs={'class':'form-control',  'placeholder':'Текст статьи', 'rows':'12', 'required': True}),
		}

class CommentsAddForm(forms.ModelForm):

	class Meta:
		model = Comments
		fields = ('text', )
		widgets = {
			'text' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Присоединиться к обсуждению'})
		}
