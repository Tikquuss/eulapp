from django import forms

class DocumentForm(forms.Form):
    docfile = forms.FileField(label='', help_text='',  required=False)