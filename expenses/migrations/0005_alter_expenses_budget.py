# Generated by Django 4.0.3 on 2022-04-19 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0003_remove_budget_saving_alter_budget_category'),
        ('expenses', '0004_alter_expenses_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenses',
            name='budget',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budget', to='budget.budget'),
        ),
    ]
