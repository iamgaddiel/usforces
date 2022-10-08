# Generated by Django 4.1.1 on 2022-10-04 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_retirement_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retirement',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('declined', 'declined'), ('approved', 'approved')], default=('pending', 'pending'), max_length=30),
        ),
    ]