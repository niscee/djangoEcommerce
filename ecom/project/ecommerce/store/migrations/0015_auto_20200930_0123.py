# Generated by Django 3.0.5 on 2020-09-29 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20200923_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customorder',
            name='date',
            field=models.DateField(help_text='Please use the following format: <em>YYYY-MM-DD</em>.', verbose_name='Required Date'),
        ),
    ]
