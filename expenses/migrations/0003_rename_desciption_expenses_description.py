# Generated by Django 4.0.3 on 2022-04-19 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_remove_expenses_expenses_title_expenses_category_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expenses',
            old_name='desciption',
            new_name='description',
        ),
    ]
