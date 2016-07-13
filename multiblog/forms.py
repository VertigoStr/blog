from django import forms
from .models import Blogger

class UserAuthForm(forms.ModelForm):

	class Meta:
		model = Blogger
		fields = ('email', 'password',)
		widgets = {
			'email': forms.EmailInput(attrs={'class':'form-control',  'placeholder':'Ваш почтовый адрес', 'required': True}),
			'password': forms.TextInput(attrs={'class':'form-control',  'placeholder':'Пароль', 'required': True}),
		}