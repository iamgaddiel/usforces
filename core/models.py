from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser
from django_quill.fields import QuillField

from django_countries.fields import CountryField



class User(AbstractUser):
	GENDER = [
		('male', 'Male'),
		('female', 'Female'),
		('other', 'Other'),
	]

	MARITAL_STATUS = [
		('single', 'Single'),
		('relationship', 'Relationship'),
		('divorce', 'Divorce'),
		('complicated', 'Complicated'),
		('married', 'Married'),
		('widowed', 'Widowed'),
	]

	DEPLOYMENT_STATUS = [
		('undeployed', 'Undeployed'),
		('processing', 'Processing'),
		('deployed', 'Deployed'),
	]

	MILITARY_RANKS = [
		('E-1', 'E-1'),
		('E-2', 'E-2'),
		('E-3', 'E-3'),
		('E-4', 'E-4'),
		('E-5', 'E-5'),
		('E-6', 'E-6'),
		('E-7', 'E-7'),
		('E-8', 'E-8'),
		('E-9', 'E-9'),
		('O-1E', 'O-1E'),
		('O-2E', 'O-2E'),
		('O-3E', 'O-3E'),
		('O-4', 'O-4'),
		('O-5', 'O-5'),
		('O-6', 'O-6'),
		('O-7', 'O-7'),
		('O-8', 'O-8'),
		('O-9', 'O-9'),
		('O-10', 'O-10'),
		('W-1', 'W-1'),
		('W-2', 'W-2'),
		('W-3', 'W-3'),
		('W-4', 'W-4'),
		('W-5', 'W-5'),
	]

	
	id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
	email = models.EmailField(unique=True)
	partners_name = models.CharField(max_length=200, blank=True)
	date_of_birth = models.DateField(null=True)
	state = models.CharField(max_length=200, null=True)
	height = models.DecimalField(decimal_places=2, max_digits=6, blank=True, null=True)
	weight = models.DecimalField(decimal_places=2, max_digits=6,  blank=True, null=True)
	marital_status = models.CharField(max_length=15, choices=MARITAL_STATUS, default='single')
	military_id = models.CharField(max_length=20, unique=True)
	rank = models.CharField(max_length=5, null=True)
	country = CountryField()
	gender = models.CharField(max_length=10, choices=GENDER)
	image = models.ImageField(upload_to='profile_image', default='main.png')
	zip_code = models.CharField(max_length=15)
	number_of_children = models.PositiveIntegerField(default=0)
	deployment_status = models.CharField(max_length=50, choices=DEPLOYMENT_STATUS, default=DEPLOYMENT_STATUS[0])
	deployment_country = CountryField(null=True)
	base = models.CharField(max_length=250, null=True)
	pay_grade = models.CharField(blank=True, null=True, choices=MILITARY_RANKS, max_length=4)
	remarks = models.TextField(null=True)


	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	def __str__(self):
		return "{first_name} {last_name}| {id}".format(
			first_name=self.first_name,
			last_name=self.last_name,
			id=self.id
		)
class Operations(models.Model):
	id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
	operation = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self) -> str:
		return self.user.username

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
	email = models.EmailField()
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
	solider_first_name = models.CharField(max_length=100)
	solider_last_name = models.CharField(max_length=100)
	solider_id_number = models.CharField(max_length=100)
	email = models.EmailField()
	internet_card_image = models.ImageField(upload_to="gift", default='gift.png')
	internet_card_number = models.CharField(max_length=100)
	internet_card_amount = models.PositiveSmallIntegerField(default=1)
	internet_card_type = models.CharField(max_length=100)
	timestamp = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=25, choices=STATUS, default=STATUS[0])

	def  __str__(self) -> str:
		return '{0} |->   {2}'.format(
			self.gift_amount,
			self.solider_id_number
		)


class News(models.Model):
	id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
	title = models.CharField(max_length=600)
	body = models.TextField()

	def __str__(self) -> str:
		return self.title


class Vacation(models.Model):
	GENDER = [
		('male', 'male'),
		('female', 'female'),
		('other', 'other'),
	]

	id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	gender = models.CharField(max_length=10, choices=GENDER)
	date_of_birth = models.DateField()
	email = models.EmailField()
	solider_id_number = models.CharField(max_length=100)
	mothers_median_name = models.CharField(max_length=30)
	relationship_with_deployed_solider = models.CharField(max_length=30)
	address = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	region = models.CharField(max_length=100)
	zip_code = models.CharField(max_length=15)
	phone = models.CharField(max_length=15)
	duration_of_vacation = models.CharField(max_length=15)
	reason_for_vacation = models.TextField()
	is_approved = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now=True)

	def __str__(self) -> str:
		return super().__str__()


class GiftCardRequest(models.Model):
	id = models.UUIDField(default=uuid4, editable=False, primary_key=True)
	amount_of_internet_card = models.DecimalField(max_digits=63, default=0, decimal_places=2)
	recipient_first_name = models.CharField(max_length=30)
	recipient_last_name = models.CharField(max_length=30)
	shipping_address_1 = models.CharField(max_length=100)
	shipping_address_2 = models.CharField(max_length=100, blank=True)
	email = models.EmailField()
	city = models.CharField(max_length=100)
	region = models.CharField(max_length=100)
	zip_code = models.CharField(max_length=15)
	phone = models.CharField(max_length=15)
	country = CountryField()
	purchasers_first_name = models.CharField(max_length=30)
	purchasers_last_name = models.CharField(max_length=30)
	billing_address_1 = models.CharField(max_length=300)
	billing_address_2 = models.CharField(max_length=300, blank=True)
	is_approved = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now=True)


	def __str__(self) -> str:
		return f"card for {self.recipient_first_name} by {self.purchasers_first_name}"
