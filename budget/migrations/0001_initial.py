# Generated by Django 4.0.3 on 2022-04-10 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BudgetChoices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget_choices', models.CharField(max_length=30, unique=True)),
                ('expiration_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('budget_choices', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budget_choices_detail', to='budget.budgetchoices')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
