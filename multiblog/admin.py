from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.db import models
from .models import Blogger, Publication, Comments, Categories
from django.core.mail import send_mail

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Blogger
        fields = ('email', )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = Blogger
		fields = ('email', 'password', 'is_active', 'is_admin', )

	def clean_password(self):
		return self.initial["password"]

class MyUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'password', 'name', 'surname', 'phone', 'skype', 'img_avatar', 'is_admin', 'is_active',)
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'surname', 'phone', 'skype', 'avatar', )}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(Blogger, MyUserAdmin)
admin.site.unregister(Group)


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'abstract', 'time', 'author', 'category',)
    ordering = ('time', 'title', 'category', )

    def save_model(self, request, obj, form, change):
        obj.save()
        if 'why_not' in form.changed_data or 'is_moderated' in form.changed_data:
            if form.instance.why_not and form.instance.is_moderated:
                print('send cancel')
                try:
                    send_mail(
                        'Публикация отклонена',
                        'Ваша публикация \"' + form.instance.title + '\" отклонена!\nПричина:\n' +
                        form.instance.why_not,
                        'testtest-14@bk.ru',
                        [form.instance.author.email],
                        fail_silently=False
                    )
                except Exception as e:
                    print(e)

            if not form.instance.is_moderated:
                print('send accept')
                try:
                    send_mail(
                        'Публикация одобрена',
                        'Ваша публикация \"' + form.instance.title + '\" одобрена!',
                        'testtest-14@bk.ru',
                        [form.instance.author.email],
                        fail_silently=False
                    )
                except Exception as e:
                    print(e)

admin.site.register(Publication, PublicationAdmin)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'time', 'publication',)
    ordering = ('time', 'author', )

admin.site.register(Comments, CommentsAdmin)

class CategoriesAdmin(admin.ModelAdmin):
    list_display=('title', 'abstract', )
    ordering = ('title', )

admin.site.register(Categories, CategoriesAdmin)