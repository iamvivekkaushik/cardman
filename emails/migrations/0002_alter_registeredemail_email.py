# Generated by Django 3.2.20 on 2023-07-18 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registeredemail',
            name='email',
            field=models.CharField(max_length=100),
        ),
    ]
