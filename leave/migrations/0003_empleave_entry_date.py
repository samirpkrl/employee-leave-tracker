# Generated by Django 3.1.1 on 2021-10-02 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0002_empleave_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleave',
            name='entry_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
