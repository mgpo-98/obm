# Generated by Django 3.2.13 on 2024-08-27 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('img', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='hashtags',
            field=models.ManyToManyField(to='img.Hashtag'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(null=True, upload_to='media/'),
        ),
    ]
