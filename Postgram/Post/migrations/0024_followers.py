# Generated by Django 4.0.5 on 2022-06-27 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0023_rename_like_post_likepost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=100)),
                ('follower', models.CharField(max_length=100)),
            ],
        ),
    ]
