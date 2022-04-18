from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from app1.models import User,City,Theatre,Movie,TimeSlot,Seat,BookingDetail
import json
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
# Create your views here.
# @api_view(['GET','POST'])

@csrf_exempt
def signup(request, *args,  **kwargs):
    try:
        user_details = {}
        user_details = json.loads(request.body)
        new_user = User(name = user_details['name'], email = user_details['email'], password = user_details['password'])
        new_user.save()
    except Exception as e:
        print(e)
        return JsonResponse({"Message": "Error in Creating User"})
    return JsonResponse({"Message": "User Signed Up Successfully"})

@csrf_exempt
def login(request, *args,  **kwargs):
    try:
        login_credentials = {}
        login_credentials = json.loads(request.body)
        authenticated_user = User.objects.get(email = login_credentials['email'], password = login_credentials['password'])
        if authenticated_user:
            return JsonResponse({"Message": "User is Authenticated SuccessFully Will Send JWT in Future"})            
    except Exception as e:
        print(e)
        return JsonResponse({"Message": "Invalid Credentials"})

@api_view(['GET'])
@csrf_exempt
def get_movies_by_city(request, city_id):
    if city_id:
        try:
            response = {}
            response['movie_details'] = []
            theatres = Theatre.objects.filter(city_id = city_id) 
            if theatres:
                for theatre in theatres:
                    movie = model_to_dict(theatre.movie)
                    theatre = model_to_dict(theatre)
                    movie_details = {
                        'theatre' : theatre,
                        'movie' : movie
                    }
                    response['movie_details'].append(movie_details)
                print("response")
                return Response(response)
            else:
                return Response({"Message": "No Movies Found"},status = 500)    
        except Exception as e:
            print(e)
            return Response({"Message": "Internal Server Error"},status = 500)
    else:
        return Response({"Message": "Invalid City Id"},status=404)

@api_view(['GET'])
@csrf_exempt
def get_cinemas_by_movie(request, movie_id):
    if movie_id:
        try:
            response = {}
            response['cinema_details'] = []
            theatres = Theatre.objects.filter(movie_id = movie_id) 
            if theatres:
                for theatre in theatres:
                    city = theatre.city
                    movie = theatre.movie
                    show_times = TimeSlot.objects.filter(theatre_id = theatre.id)
                    theatre_show_times = []
                    for show_time in show_times:
                        theatre_show_times.append(model_to_dict(show_time,fields=["id","time"]))
                    theatre = model_to_dict(theatre, fields = ["id","name"])
                    theatre['city'] = city.name
                    theatre['movie'] = movie.name
                    movie_details = {
                        'theatre' : theatre,
                        'showTimings' : theatre_show_times
                    }
                    response['cinema_details'].append(movie_details)
                return Response(response)
            else:
                return Response({"Message": "No cinema Found"},status = 500)    
        except Exception as e:
            print(e)
            return Response({"Message": "Internal Server Error"},status = 500)
    else:
        return Response({"Message": "Invalid Movie Id"},status=404)

@api_view(['POST'])
@csrf_exempt
def generate_seats(request):
    input_details = json.loads(request.body)
    try:
        slot_id = input_details['slotId']
        no_of_seats = input_details['noOfSeats']
        if slot_id:
            show_time = TimeSlot.objects.get(id = slot_id)
            theatre = show_time.theatre
            print(theatre.id)
            if show_time:
                for i in range(1,no_of_seats + 1):
                    Seat(number = i, theatre = theatre, time_slot = show_time).save()
                return Response({"Messsage" : "Seats Generated Successfully"})
            else:
                return Response({"Messsage" : "COuldnt Find the Show"}, status = 401)
        else:
            return Response({"Messsage" : "Invalid Request"}, status = 401)
    except Exception as e:
        print(e)
        return Response({"Messsage" : "Internal Error"}, status = 500)

@api_view(['GET'])
@csrf_exempt
def view_seats(request, slot_id):
    try:
        if slot_id:
            show = TimeSlot.objects.get(id = slot_id)
            if show:
                seats = []
                Seats = Seat.objects.filter(time_slot = show)
                for seat in Seats:
                    seat = model_to_dict(seat, fields=["id","number","booking_status"])
                    seats.append(seat)
                theatre = show.theatre
                cinema = model_to_dict(theatre, fields=["id","name"])
                movie = model_to_dict(theatre.movie, fields=["id","name"])
                city = model_to_dict(theatre.city, fields=["id","name"])
                response = {
                    "cinema" : cinema,
                    "movie" : movie,
                    "show" : show.time,
                    "seats" : seats
                }
                return Response(response)
            else:
                return Response({"Message" : "Couldnt Find Show"}, status = 400)
        else:
            return Response({"Message" : "Invalid Slot Id"})
    except Exception as e:
        print(e)
        return Response({"Message" : "Internal Server Error"}, status = 500)

@api_view(['POST'])
@csrf_exempt
def book_ticket(request, seat_id):
    try:
        seat = Seat.objects.get(id = seat_id)
        if seat.booking_status == False:
            seat.booking_status = True
            theatre = seat.theatre
            movie = theatre.movie
            city = theatre.city
            time_slot = seat.time_slot
            booking_details = BookingDetail(seat = seat,time_slot = time_slot,theatre = theatre,movie = movie)
            booking_details.save()
            seat.save()
            response = {
                "booking_details" : model_to_dict(booking_details),
                "movie" : model_to_dict(movie),
                "theatre" : model_to_dict(theatre),
                "showTime" : model_to_dict(time_slot),
                "seat" : model_to_dict(seat)
            }
            return Response(response)
        else:
            return Response({"Message" : "Seat Already Booked"})    
    except Exception as e:
        print(e)
        return Response({"Message" : "Internal Server Error"}, status = 500)


@api_view(['GET'])
@csrf_exempt
def booking_details(request, booking_id):
    try:
        booking_details = BookingDetail.objects.get(id = booking_id)
        response = model_to_dict(booking_details)
        return Response(response)
    except Exception as e:
        return Response({"Message" : "Internal Server Error"}, status = 500)