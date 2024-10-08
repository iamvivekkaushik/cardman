# Generated by Django 4.2.16 on 2024-10-02 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_card_account_type_card_is_active_alter_card_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Is Paid'),
        ),
        migrations.AddField(
            model_name='card',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified At'),
        ),
    ]
