# Generated by Django 4.0.4 on 2022-04-14 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_rename_seats_seat_rename_name_seat_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.movie')),
                ('seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.seat')),
                ('theatre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.theatre')),
                ('time_slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.timeslot')),
            ],
        ),
    ]
