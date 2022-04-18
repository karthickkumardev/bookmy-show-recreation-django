from django.urls import path

from . import views
# from .views import api_home


urlpatterns = [
    path('signup', views.signup),
    path('login', views.login),
    path('movies/<int:city_id>', views.get_movies_by_city),
    path('cinemas/<int:movie_id>', views.get_cinemas_by_movie),
    path('seats/add',views.generate_seats),
    path('seats/<int:slot_id>',views.view_seats),
    path('book/<int:seat_id>',views.book_ticket),
    path('booking/details/<int:booking_id>',views.booking_details)

    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('', views.api_home), # localhost:8000/api/
    # path('products/', include('products.urls'))
]