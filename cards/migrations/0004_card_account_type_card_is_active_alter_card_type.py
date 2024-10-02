# Generated by Django 4.2.16 on 2024-10-02 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_auto_20230718_0542'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='account_type',
            field=models.CharField(choices=[('CC', 'Credit Card'), ('DC', 'Debit Card'), ('PP', 'Prepaid Card'), ('VC', 'Virtual Card')], default='CC', max_length=2),
        ),
        migrations.AddField(
            model_name='card',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is Active'),
        ),
        migrations.AlterField(
            model_name='card',
            name='type',
            field=models.CharField(choices=[('VISA', 'Visa'), ('RUPY', 'RuPay'), ('MSTR', 'Master Card'), ('DMFK', 'DreamFolks'), ('PRPS', 'Priority Pass'), ('MTRO', 'Metro Card')], default='VISA', max_length=4),
        ),
    ]
