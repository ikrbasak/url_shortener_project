import logging
from http import HTTPStatus

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.gzip import gzip_page
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from ratelimit.decorators import ratelimit

import shortener_app.settings as app_settings
from .forms import UrlSubmitForm
from .models import KeyValidator, UrlValidator, UrlSaveModel


def create_key(url: str, l: int = app_settings.DEFAULT_KEY_LENGTH) -> str:
    u = url + app_settings.date_time() + app_settings.random_salt()
    h = app_settings.hasher(u)
    k = h[-l:]
    key_validator = KeyValidator(to_return=True)
    if not key_validator(k)[0]:
        k = create_key(u, l)
    return k


def default_context() -> dict:
    def_context = {
        "author": {
            "name": "Krishna Basak",
            "contact": {
                "linkedin": "https://www.linkedin.com/in/ikrbasak",
                "github": "https://github.com/ikrbasak/",
                "mail": "ikrbasa.k+url.shortener@gmail.com"
            }
        },
        "project": {
            "name": "compli",
            "github": "https://github.com/ikrbasak/url_shortener_project"
        }
    }
    return def_context


@require_GET
@gzip_page
def index_view(request, extras=None):
    context = {
        "url_form": UrlSubmitForm()
    }

    if extras is not None:
        logging.info(extras)
        context['extras'] = extras
    context['default'] = default_context()

    return render(request, 'shortener_app/index_view.html', context)


@require_POST
@gzip_page
@ratelimit(key='user_or_ip', rate='600/60m', method=['POST'])
def url_submit_view(request):
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return JsonResponse({
            "error": True,
            "error_desc": "Crossed the limit of creating short URLs per hour",
            "error_code": "limit_crossed"
        }, status=HTTPStatus.BAD_REQUEST)

    else:
        key_validator = KeyValidator(to_return=True)
        url_validator = UrlValidator(to_return=True)

        form_data = UrlSubmitForm(request.POST)
        if form_data.is_valid():
            key = form_data.data['key_field']
            url = form_data.data['url_field']

            # First - Check if the URL is OK
            flag, message, code = url_validator(url)
            if not flag:
                return JsonResponse({
                    "error": True,
                    "error_desc": message,
                    "error_code": code
                }, status=HTTPStatus.BAD_REQUEST)

            # If no key provided, create a key
            if key == '':
                key = create_key(url)
            # else, validate the provided key
            else:
                flag, message, code = key_validator(key)
                if not flag:
                    return JsonResponse({
                        "error": True,
                        "error_desc": message,
                        "error_code": code
                    }, status=HTTPStatus.BAD_REQUEST)

            try:
                save_url = UrlSaveModel(key=key, url=url)
                save_url.save()

            except KeyError or Exception:
                return JsonResponse({
                    "error": True,
                    "error_desc": 'Cannot save to the database',
                    "error_code": 'db_error'
                }, status=HTTPStatus.INTERNAL_SERVER_ERROR)

            return JsonResponse({
                "error": False,
            }, status=HTTPStatus.OK)

        else:
            return JsonResponse({
                "error": True,
                "error_desc": "Provided invalid form data",
                "error_code": "invalid_form"
            }, status=HTTPStatus.BAD_REQUEST)


@require_http_methods(['POST', 'GET'])
def url_query_view(request, key):
    saved_url = UrlSaveModel.objects.filter(key__exact=key)
    l = len(saved_url)
    url = None

    if l > 0:
        saved_url = saved_url[0]
        url = saved_url.url
    else:
        pass

    if request.method == 'POST':
        if url is None:
            return JsonResponse({
                'error': True,
                'error_desc': 'The URL with provided key not found',
                'error_code': 'url_not_found'
            }, status=HTTPStatus.NOT_FOUND)
        else:
            return JsonResponse({
                'error': False,
                'key': key,
                'url': url,
            }, status=HTTPStatus.OK)

    elif request.method == 'GET':
        if url is None:
            return HttpResponse('Error', status=HTTPStatus.NOT_FOUND)
        else:
            return redirect(url, status=HTTPStatus.OK)
