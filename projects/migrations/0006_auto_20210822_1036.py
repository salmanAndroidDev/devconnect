# Generated by Django 3.1.4 on 2021-08-22 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_username'),
        ('projects', '0005_review_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='owner',
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.profile'),
        ),
    ]
