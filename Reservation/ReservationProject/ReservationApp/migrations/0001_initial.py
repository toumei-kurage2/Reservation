# Generated by Django 4.1 on 2024-07-11 02:18

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
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility_name', models.CharField(max_length=50)),
                ('picture_url', models.URLField()),
            ],
            options={
                'db_table': 'facility',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ReservationApp.account')),
            ],
            options={
                'db_table': 'reseravtion',
            },
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=30)),
                ('capacity', models.IntegerField()),
                ('type_fee', models.IntegerField()),
            ],
            options={
                'db_table': 'roomtype',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.IntegerField()),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ReservationApp.facility')),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ReservationApp.roomtype')),
            ],
            options={
                'db_table': 'room',
            },
        ),
        migrations.CreateModel(
            name='Reservation_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('type_persons', models.IntegerField()),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ReservationApp.reservation')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ReservationApp.room')),
            ],
            options={
                'db_table': 'reservation_detail',
                'unique_together': {('room', 'date')},
            },
        ),
    ]
