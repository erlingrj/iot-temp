# Generated by Django 2.2 on 2019-05-08 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='choice',
            old_name='chioce_test',
            new_name='choice_test',
        ),
    ]
