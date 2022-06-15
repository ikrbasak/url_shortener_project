import re

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import models
from django.utils.deconstruct import deconstructible
from django_extensions.db.models import TimeStampedModel

import shortener_app.settings as app_settings


@deconstructible
class KeyValidator:
    regex = re.compile(r'[^a-zA-Z0-9_-]')
    max_len = app_settings.MAX_KEY_LENGTH
    min_len = app_settings.MIN_KEY_LENGTH

    @staticmethod
    def __key_exists__(key):
        all_keys = [k[0] for k in UrlSaveModel.objects.values_list('key')]
        return key in all_keys

    def __init__(self, to_return: bool = False):
        self.to_return = to_return

    def __call__(self, value: str):
        l = len(value)

        if l > self.max_len:
            msg, code = (f'The key \'{value}\' has length {l} '
                         f'but maximum length allowed is {self.max_len}',
                         'max_len_exceeded')
            if self.to_return:
                return False, msg, code
            else:
                raise ValidationError(msg, code)

        elif l < self.min_len:
            msg, code = (f'The key \'{value}\' has length {l} '
                         f'but minimum length need to be {self.min_len}',
                         'min_len_not_met')
            if self.to_return:
                return False, msg, code
            else:
                raise ValidationError(msg, code)

        elif self.regex.search(value):
            msg, code = (f'The key \'{value}\' has invalid characters',
                         'invalid_chars')
            if self.to_return:
                return False, msg, code
            else:
                raise ValidationError(msg, code)

        elif self.__key_exists__(value):
            msg, code = (f'Use another key', 'key_exists')
            if self.to_return:
                return False, msg, code
            else:
                raise ValidationError(msg, code)
        else:
            msg = 'The key is OK to process further'
            code = 'key_ok'
            return True, msg, code


class UrlValidator(URLValidator):
    def __init__(self, to_return: bool = False, **kwargs):
        self.to_return = to_return
        super().__init__(**kwargs)

    def __call__(self, value: str):
        if self.to_return:
            try:
                super(UrlValidator, self).__call__(value)
                msg = 'The key is OK to process further'
                code = 'key_ok'
                return True, msg, code
            except ValidationError:
                msg, code = 'The URL mentioned is invalid', 'invalid_url'
                return False, msg, code
        else:
            super(UrlValidator, self).__call__(value)


# Create your models here.
class UrlSaveModel(TimeStampedModel):
    key_validator = KeyValidator(to_return=False)
    url_validator = UrlValidator(to_return=False)

    key = models.CharField(
        max_length=app_settings.MAX_KEY_LENGTH,
        primary_key=True, unique=True,
        null=False, blank=False,
        verbose_name='Key', help_text='Unique key for the URL',
        validators=[key_validator]
    )
    url = models.URLField(
        max_length=app_settings.MAX_URL_LENGTH, unique=False,
        blank=False, null=False,
        verbose_name='URL', help_text='The URL to be shortened',
        validators=[url_validator]
    )

    class Meta:
        verbose_name = 'Saved URL'
        verbose_name_plural = 'Saved URLs'
        ordering = ('key', 'url', 'created', 'modified')

    def __str__(self):
        return self.key

    def __repr__(self):
        return f'[{self.key}] {self.url}'
