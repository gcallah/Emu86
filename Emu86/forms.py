from django import forms


class MainForm(forms.Form):
    code = forms.CharField(required = False, 
    	                   widget=forms.Textarea(attrs={
                                            'cols': 60,
                                            'rows': 24, 
                                            'oninput': 'checkForScript()'}))
