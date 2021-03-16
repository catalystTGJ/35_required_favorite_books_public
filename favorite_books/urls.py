from django.urls import path, include

urlpatterns = [
    path('', include('login_app.urls')),
    path('', include('favorite_books_app.urls')),
]
