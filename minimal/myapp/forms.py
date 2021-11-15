from django import forms


class DocumentForm(forms.Form):
    name = forms.CharField(label='Nome', max_length=100)
    surename = forms.CharField(label='Cognome', max_length=100)
    classe = forms.CharField(label='Gruppo', max_length=100)
    docfile = forms.FileField(label='Seleziona il video')
