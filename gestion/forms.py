from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User
from rrhh.models.base import Perfil
from rrhh.models.entidad import Entidad
from rrhh.models.persona import NIVEL_ACCESO


class EntidadForm(forms.ModelForm):
    class Meta:
        model = Entidad
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(EntidadForm, self).__init__(*args, **kwargs)
        self.fields['direccion'].widget.attrs['required'] = True
        self.fields['dependiente'].widget.attrs['required'] = True
        self.helper = FormHelper()
        self.helper.form_tag = False


class UserForm(forms.ModelForm):
    """
        Formulario para crear un usuario
    """

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]
        widgets = {
            'password': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False


class CambiarPerfilUsuarioForm(forms.Form):
    perfil = forms.ModelChoiceField(
        queryset=Perfil.objects.all(),
        label="Perfil"
    )
    nivel_acceso = forms.ChoiceField(
        choices=NIVEL_ACCESO,
        label="Nivel de acceso"
    )

    def __init__(self, *args, **kwargs):
        super(CambiarPerfilUsuarioForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
