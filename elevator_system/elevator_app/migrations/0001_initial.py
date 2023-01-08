# Generated by Django 4.1.5 on 2023-01-08 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FloorRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.CharField(choices=[('UP', 'Up'), ('DOWN', 'Down')], max_length=4)),
                ('floor', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Elevator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movement', models.CharField(choices=[('UP', 'Up'), ('DOWN', 'Down'), ('STOPPED', 'Stopped')], default='STOPPED', max_length=8)),
                ('floor', models.PositiveIntegerField()),
                ('doors_open', models.BooleanField(default=False)),
                ('available', models.BooleanField(default=True)),
                ('operational', models.BooleanField(default=True)),
                ('requests', models.ManyToManyField(blank=True, to='elevator_app.floorrequest')),
            ],
        ),
    ]