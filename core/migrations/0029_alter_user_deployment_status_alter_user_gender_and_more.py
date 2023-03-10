# Generated by Django 4.1.3 on 2023-03-10 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_user_pay_grade_alter_user_rank_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='deployment_status',
            field=models.CharField(choices=[('undeployed', 'Undeployed'), ('processing', 'Processing'), ('deployed', 'Deployed')], default=('undeployed', 'Undeployed'), max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='height',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='marital_status',
            field=models.CharField(choices=[('single', 'Single'), ('relationship', 'Relationship'), ('divorce', 'Divorce'), ('complicated', 'Complicated'), ('married', 'Married'), ('widowed', 'Widowed')], default='single', max_length=15),
        ),
        migrations.AlterField(
            model_name='user',
            name='pay_grade',
            field=models.CharField(blank=True, choices=[('E-1', 'E-1'), ('E-2', 'E-2'), ('E-3', 'E-3'), ('E-4', 'E-4'), ('E-5', 'E-5'), ('E-6', 'E-6'), ('E-7', 'E-7'), ('E-8', 'E-8'), ('E-9', 'E-9'), ('O-1E', 'O-1E'), ('O-2E', 'O-2E'), ('O-3E', 'O-3E'), ('O-4', 'O-4'), ('O-5', 'O-5'), ('O-6', 'O-6'), ('O-7', 'O-7'), ('O-8', 'O-8'), ('O-9', 'O-9'), ('O-10', 'O-10'), ('W-1', 'W-1'), ('W-2', 'W-2'), ('W-3', 'W-3'), ('W-4', 'W-4'), ('W-5', 'W-5')], max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]