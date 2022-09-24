from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	ROLE = [
		('admin', 'admin'),
		('client', 'client')
	]
	id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
	email = models.EmailField(unique=True)
	role = models.CharField(max_length=6)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	def __str__(self):
		return super().__str__()
