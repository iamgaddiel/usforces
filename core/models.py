from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

from django_countries.fields import CountryField



class User(AbstractUser):
	GENDER = [
		('male', 'male'),
		('female', 'female'),
		('other', 'other'),
	]

	
	id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
	email = models.EmailField(unique=True)
	military_id = models.CharField(max_length=20, unique=True)
	country = CountryField()
	gender = models.CharField(max_length=10, choices=GENDER)
	image = models.ImageField(upload_to='profile_image', default='main.png')
	zip_code = models.CharField(max_length=15)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	def __str__(self):
		return super().__str__()


class Retirement(models.Model):
	STATUS = [
		('pending', 'pending'),
		('declined', 'declined'),
		('approved', 'approved')
	]
	
	id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	address = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	region = models.CharField(max_length=100)
	zip_code = models.CharField(max_length=15)
	phone_number = models.CharField(max_length=15)
	email = models.EmailField()
	ceremony_date  = models.DateField()
	rank = models.CharField(max_length=10)
	branch_of_service = models.CharField(max_length=50)
	years_of_service = models.PositiveSmallIntegerField()
	date_of_retirement = models.DateField()
	additional_information =  models.TextField()
	timestamp = models.DateTimeField(auto_now=True)
	is_approved = models.BooleanField(default=False)
	status = models.CharField(max_length=10, choices=STATUS)

	def  __str__(self) -> str:
		return '{0} {2}  retirement form'

