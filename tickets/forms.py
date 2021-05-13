from django import forms


class ValidateResponse(forms.Form):
    text = forms.CharField(error_messages={'required': 'Reply can not be empty'})

    def clean(self):
        text = str(self.cleaned_data.get('text'))
        if text is None:
            raise forms.ValidationError('Reply can not be empty')
        return True


class ValidateTicket(forms.Form):
    title = forms.CharField(error_messages={'required': 'Title can not be empty'})
    text = forms.CharField(error_messages={'required': 'Description can not be empty'})

    def clean(self):
        title = str(self.cleaned_data.get('title'))
        text = str(self.cleaned_data.get('text'))
        if text is None or title is None:
            raise forms.ValidationError('Reply or title can not be empty')
        return True
