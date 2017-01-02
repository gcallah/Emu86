from django import forms


class MainForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea)
