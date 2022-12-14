# Generated by Django 4.1.1 on 2022-10-02 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_retirement_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Replacement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name_of_soldier', models.CharField(max_length=100)),
                ('rank_of_soldier', models.CharField(max_length=100)),
                ('base_of_current_service', models.CharField(max_length=100)),
                ('destination_after_replacement', models.CharField(max_length=100)),
                ('name_of_applicant', models.CharField(max_length=100)),
                ('country_of_origin_or_location', django_countries.fields.CountryField(max_length=2)),
                ('relationship_to_the_soldier', models.CharField(max_length=100)),
                ('applicants_id_number', models.CharField(max_length=100)),
                ('applicants_address', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('declined', 'declined'), ('approved', 'approved')], default=('pending', 'pending'), max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
