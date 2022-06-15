from django import forms

import shortener_app.settings as app_settings


class UrlSubmitForm(forms.Form):
    url_field = forms.CharField(
        max_length=app_settings.MAX_URL_LENGTH,
        min_length=app_settings.MIN_URL_LENGTH,
        label="Long URL",
        label_suffix=":",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": 'text_input',
                "id": 'url_input',
                "placeholder": '',
            }
        )
    )
    key_field = forms.CharField(
        max_length=app_settings.MAX_KEY_LENGTH,
        min_length=app_settings.MIN_KEY_LENGTH,
        label="Short Key",
        label_suffix=":",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": 'text_input',
                "id": 'key_input',
                "placeholder": '',
            }
        )
    )
