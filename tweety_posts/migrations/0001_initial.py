# Generated by Django 5.1.1 on 2024-09-23 07:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500, null=True)),
                ('image', models.ImageField(null=True, upload_to='posts/images')),
                ('date', models.DateField(auto_now=True)),
                ('time', models.TimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='accounts.profile')),
                ('like', models.ManyToManyField(related_name='post_liked_by', to='accounts.profile')),
            ],
        ),
    ]