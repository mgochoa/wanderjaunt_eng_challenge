# Generated by Django 4.0.2 on 2022-02-08 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Turn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField()),
                ('scheduled_for', models.DateField()),
                ('is_same_day', models.BooleanField()),
            ],
        ),
    ]