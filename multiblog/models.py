from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class BloggerManager(BaseUserManager):
	def create_user(self, email, password):
		if not email:
			raise ValueError('Blogger must have an email address')

		user = self.model(email = self.normalize_email(email), )
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password):
		user = self.create_user(email, password=password, )
		user.is_admin = True
		user.save(using=self._db)
		return user

class Blogger(AbstractBaseUser):
	email = models.EmailField(verbose_name='Email', unique=True, max_length=250)
	name = models.CharField(max_length=100, verbose_name='Имя', blank=True)
	surname = models.CharField(max_length=100, verbose_name='Фамилия', blank=True)
	phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True)
	skype = models.CharField(max_length=20, verbose_name='Skype', blank=True)
	avatar = models.ImageField(upload_to=u'./media/img/', verbose_name='Аватар', blank=False, default='./media/img/ava-default.png')

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = BloggerManager()

	USERNAME_FIELD = 'email'

	def get_full_name(self):
		if self.name or self.surname:
			return self.name + " " + self.surname
		else:
			return self.email

	def get_short_name(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return self.is_admin			

	def has_module_perms(self, app_label):
		return self.is_admin			

	@property
	def is_staff(self):
		return self.is_admin


	def img_avatar(self):
		if self.avatar:
			return '<img src="%s" width="100"/>' % self.avatar.url
		else:
			return '(none)'

	img_avatar.short_description = 'Аватар'
	img_avatar.allow_tags = True

	class Meta:
		verbose_name = u'Блоггер'
		verbose_name_plural = u'Блоггеры'

	def __str__(self):
		if self.name or self.surname:
			return self.name + " " + self.surname
		else:
			return self.email


class Publication(models.Model):
	title = models.CharField(max_length=200, verbose_name='Имя')
	abstract = models.TextField(max_length=600, verbose_name='Краткое содержание')
	full_text = models.TextField(verbose_name='Полное описание')
	time = models.DateTimeField(verbose_name='Дата публикации')
	author = models.ForeignKey('Blogger', on_delete=models.CASCADE, verbose_name='Автор')

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = u'Публикация'
		verbose_name_plural = u'Публикации'
		
class Comments(models.Model):
	text = models.TextField(verbose_name='Текст')
	time = models.DateTimeField(verbose_name='Дата публикации')
	author = models.ForeignKey('Blogger', on_delete=models.CASCADE, verbose_name='Автор')
	publication = models.ForeignKey('Publication', on_delete=models.CASCADE, verbose_name='Публикация')

	def __str__(self):
		return self.text

	class Meta:
		verbose_name = u'Комментарий'
		verbose_name_plural = u'Комментарии'			