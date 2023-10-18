# Generated by Django 3.2.13 on 2023-10-16 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='post_images/')),
                ('gif', models.FileField(blank=True, null=True, upload_to='post_gifs/')),
                ('hashtags', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]
