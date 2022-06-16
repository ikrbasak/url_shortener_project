from django.urls import path

from .views import (index_view, url_submit_view, url_query_view)

urlpatterns = [
    path('', index_view, name='shortener_app.index_view'),
    path('submit', url_submit_view, name='shortener_app.url_submit_view'),
    path('<str:key>', url_query_view, name='shortener_app.url_query_view'),
    path('<str:key>', url_query_view, name='shortener_app.url_query_view'),
]
