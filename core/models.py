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
		return "{first_name} {last_name}| {id}".format(
			first_name=self.first_name,
			last_name=self.last_name,
			id=self.id
		)


class Retirement(models.Model):
	STATUS = [
		('pending', 'pending'),
		('declined', 'declined'),
		('approved', 'approved')
	]
	
	id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
	# user = models.ForeignKey(User, on_delete=models.CASCADE)
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
	status = models.CharField(max_length=30, choices=STATUS, default=STATUS[0])

	def  __str__(self) -> str:
		return '{0} {2}  retirement form'.format(
			self.first_name,
			self.last_name
		)


class Replacement(models.Model):
	STATUS = [
		('pending', 'pending'),
		('declined', 'declined'),
		('approved', 'approved')
	]
	
	id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
	# user = models.ForeignKey(User, on_delete=models.CASCADE)
	name_of_soldier = models.CharField(max_length=100)
	rank_of_soldier = models.CharField(max_length=100)
	base_of_current_service =  models.CharField(max_length=100)
	destination_after_replacement = models.CharField(max_length=100)
	name_of_applicant = models.CharField(max_length=100)
	country_of_origin_or_location =  CountryField()
	relationship_to_the_soldier = models.CharField(max_length=100)
	applicants_id_number = models.CharField(max_length=100)
	applicants_address = models.CharField(max_length=100)
	timestamp = models.DateTimeField(auto_now=True)
	is_approved = models.BooleanField(default=False)
	status = models.CharField(max_length=25, choices=STATUS, default=STATUS[0])

	def  __str__(self) -> str:
		return '{0} |->   {2} | {3}'.format(
			self.name_of_soldier,
			self.name_of_applicant,
			self.timestamp
		)


class Gift(models.Model):
	STATUS = [
		('pending', 'pending'),
		('declined', 'declined'),
		('approved', 'approved')
	]

	id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
	# user = models.ForeignKey(User, on_delete=models.CASCADE)
	solder_first_name = models.CharField(max_length=100)
	solder_last_name = models.CharField(max_length=100)
	solders_id_number = models.CharField(max_length=100)
	# gift_card_to = models.ForeignKey(User, models.CASCADE, related_name='gift_to')
	gift_image = models.ImageField(upload_to="gift", default='gift.png')
	git_card_number = models.CharField(max_length=100)
	gift_card_amount = models.PositiveSmallIntegerField(default=1)
	gift_card_type = models.CharField(max_length=100)
	timestamp = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=25, choices=STATUS, default=STATUS[0])

	def  __str__(self) -> str:
		return '{0} |->   {2}'.format(
			self.gift_amount,
			self.solders_id_number
		)

