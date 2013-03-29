from django import forms
from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from leechy.models import ShoutboxMessage


class ShoutboxMessageForm(forms.ModelForm):

    message = forms.CharField(widget=forms.Textarea, label='')

    def __init__(self, *args, **kwargs):
        super(ShoutboxMessageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('send', _('Send')))

    class Meta:
        model = ShoutboxMessage
        exclude = ['author']
