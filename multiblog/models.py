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
	name = models.CharField(max_length=100, verbose_name='Имя')
	surname = models.CharField(max_length=100, verbose_name='Фамилия')
	phone = models.CharField(max_length=20, verbose_name='Телефон')
	skype = models.CharField(max_length=20, verbose_name='Skype')
	avatar = models.ImageField(upload_to=u'./media/img/', verbose_name='Аватар')

	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = BloggerManager()

	USERNAME_FIELD = 'email'

	def get_full_name(self):
		return self.email

	def get_short_name(self):
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

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

	def __str__(self):
		if self.name and self.surname:
			return self.name + " " + self.surname
		else:
			return self.email
