# Generated by Django 4.0.5 on 2022-06-23 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0018_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='Relationship_status',
            field=models.CharField(choices=[('None', 'None'), ('Single', 'Single'), ('In a relationship', 'In a relationship'), ('Married', 'Married'), ('Engaged', 'Engaged')], default=None, max_length=20),
        ),
    ]
