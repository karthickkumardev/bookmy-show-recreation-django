from django.db import models

class User(models.Model):
    name = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    password = models.CharField(max_length=120)

    def __str__(self):
        return self.email

class City(models.Model):
    name = models.CharField(max_length=120)

class Movie(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class Theatre(models.Model):
    name = models.CharField(max_length=120)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,null=True) 

class TimeSlot(models.Model):
    time = models.CharField(max_length=120)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)

class Seat(models.Model):
    number = models.CharField(max_length=120)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot,on_delete=models.CASCADE)
    booking_status = models.BooleanField(default="False")

class BookingDetail(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot,on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat,on_delete=models.CASCADE)
