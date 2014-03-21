from django import forms
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Fieldset
from models import Suggestion


class SuggestForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ("url", "email", "notes")

    def __init__(self, *args, **kwargs):

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse("suggest")
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-6'

        self.helper.layout = Layout(
            Fieldset(
                'WMS service suggestion',
                'url', 'email', 'notes',
            ),
            ButtonHolder(
                Submit('save', 'Send', css_class='btn btn-large btn-primary pull-right')
            )
        )
        return super(SuggestForm, self).__init__(*args, **kwargs)