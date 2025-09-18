from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    """
    Um formulário de criação de usuário personalizado.
    Adicionamos o campo de e-mail e o tornamos obrigatório.
    """
    email = forms.EmailField(
        required=True,
        help_text='Obrigatório. Um e-mail válido para contato.'
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Adicionando classes do Tailwind CSS para estilizar os campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'w-full px-4 py-2 mt-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'


class CustomAuthenticationForm(AuthenticationForm):
    """
    Um formulário de login personalizado para aplicar estilos.
    """
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)
        # Adicionando classes do Tailwind CSS para estilizar os campos
        self.fields['username'].widget.attrs.update(
            {'class': 'w-full px-4 py-2 mt-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Nome de usuário'}
        )
        self.fields['password'].widget.attrs.update(
            {'class': 'w-full px-4 py-2 mt-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Senha'}
        )
        self.fields['remember_me'] = forms.BooleanField(
            required=False,
            widget=forms.CheckboxInput(attrs={'class': 'mr-2 leading-tight'}),
            label='Lembrar-me'
        )
        self.fields['remember_me'].widget.attrs.update({'class': 'mr-2 leading-tight'})

class ShippingForm(forms.Form):
    """
    Formulário para coletar dados de entrega do cliente.
    """
    name = forms.CharField(label='Nome Completo', max_length=100, required=True)
    email = forms.EmailField(label='E-mail', max_length=100, required=True)
    address = forms.CharField(label='Endereço de Entrega', max_length=255, required=True)

    def __init__(self, *args, **kwargs):
        super(ShippingForm, self).__init__(*args, **kwargs)
        # Adiciona classes do Tailwind para estilização
        self.fields['name'].widget.attrs.update(
            {'class': 'w-full px-4 py-2 mt-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}
        )
        self.fields['email'].widget.attrs.update(
            {'class': 'w-full px-4 py-2 mt-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}
        )
        self.fields['address'].widget.attrs.update(
            {'class': 'w-full px-4 py-2 mt-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}
        )
