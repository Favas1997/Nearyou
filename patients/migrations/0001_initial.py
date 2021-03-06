# Generated by Django 3.2 on 2021-06-20 04:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Admin1', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='patients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20, unique=True)),
                ('place', models.CharField(max_length=100)),
                ('age', models.IntegerField(null=True)),
                ('gender', models.CharField(max_length=8, null=True)),
                ('blood_group', models.CharField(max_length=4, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='chatroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roomcode', models.TextField(blank=True, null=True)),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Admin1.doctors')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('slot', models.CharField(blank=True, max_length=20, null=True)),
                ('amount', models.CharField(max_length=10)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('Room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patients.chatroom')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin1.doctors')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patients')),
            ],
        ),
    ]
