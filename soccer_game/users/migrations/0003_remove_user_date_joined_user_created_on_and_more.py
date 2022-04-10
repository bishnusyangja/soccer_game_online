# Generated by Django 4.0.3 on 2022-04-10 17:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='date_joined',
        ),
        migrations.AddField(
            model_name='user',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created on'),
        ),
        migrations.AddField(
            model_name='user',
            name='modified_on',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Modified on'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30, verbose_name='first name'),
        ),
    ]
