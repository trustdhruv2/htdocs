# Generated by Django 3.2.10 on 2021-12-28 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=13)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Active contacts',
            },
        ),
        migrations.CreateModel(
            name='other_details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.SmallIntegerField(choices=[(0, 'Male'), (1, 'Female'), (2, 'Other')])),
                ('address', models.TextField()),
                ('active_contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.contacts')),
            ],
            options={
                'verbose_name_plural': 'Other details',
            },
        ),
        migrations.CreateModel(
            name='school',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('location', models.TextField()),
                ('joined_on', models.DateField()),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='states',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.school')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.other_details')),
            ],
        ),
        migrations.AddField(
            model_name='other_details',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.states'),
        ),
        migrations.AddField(
            model_name='other_details',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]