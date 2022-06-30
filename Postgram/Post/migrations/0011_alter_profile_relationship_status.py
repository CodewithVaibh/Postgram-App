# Generated by Django 4.0.5 on 2022-06-17 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0010_alter_profile_relationship_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='Relationship_status',
            field=models.CharField(blank=True, choices=[('0', 'None'), ('1', 'Single'), ('2', 'In a relationship'), ('3', 'Married'), ('4', 'Engaged')], max_length=2),
        ),
    ]
