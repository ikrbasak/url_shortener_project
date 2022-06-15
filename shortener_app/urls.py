from django.urls import path

from .views import index_view, url_submit_view

urlpatterns = [
    path('submit', url_submit_view, name='shortener_app.url_submit_view'),
    path('', index_view, name='shortener_app.index_view'),
]
