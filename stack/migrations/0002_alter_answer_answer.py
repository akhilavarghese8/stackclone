# Generated by Django 4.1.4 on 2023-02-17 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stack', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=models.CharField(max_length=200),
        ),
    ]
