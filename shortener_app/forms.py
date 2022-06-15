from django import forms


class UrlSubmitForm(forms.Form):
    url_field = forms.CharField()
    key_field = forms.CharField()
