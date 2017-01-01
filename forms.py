from django import forms


class MainForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea)
    output = forms.CharField(max_length=60)
