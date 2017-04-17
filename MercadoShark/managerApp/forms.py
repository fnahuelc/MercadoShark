from django import forms
from django.contrib.auth.models import User

from .models import Item


class ItemForm(forms.ModelForm):
    styles = {'class':'form-control',
                     'style':
                         'width:80%;'
                         'margin:auto;'}

    title = forms.CharField(
        widget=forms.TextInput(
            attrs = styles
        ),
        initial='oculos Ray Ban Aviador  Que Troca As Lentes  Lancamento!'
    )

    category_id = forms.CharField(
        widget=forms.Select(
            attrs=styles,
            choices=([
       ('MLA11066', 'Accesorios para Vehiculos'),
       ('MLA11066', 'Animales y Mascotas'),
       ('MLA11066', 'Antiguedades'),
    ])))

    price = forms.FloatField(
        widget=forms.TextInput(
            attrs=styles
        ),
        initial=289
    )
    currency_id = forms.CharField(
        widget=forms.TextInput(
            attrs=styles
        ),
        initial='ARS'
    )

    available_quantity = forms.IntegerField(
        widget=forms.TextInput(
            attrs=styles
        ),
        initial=64
    )

    buying_mode = forms.CharField(
        widget=forms.Select(
            attrs=styles,
            choices=([
       ('buy_it_now', 'Comprar ahora'),
       ('buy_it_now', 'Otro (no disponible)'),
    ])))


    listing_type_id = forms.CharField(
        widget=forms.Select(
            attrs=styles,
            choices=([
       ('gold_special', 'Oro especial'),
       ('gold_special', 'Otro (no disponible)'),
    ])))

    condition = forms.CharField(
        widget=forms.Select(
            attrs=styles,
            choices=([
       ('new', 'Nuevo'),
       ('used', 'Usado'),
    ])))


    description = forms.CharField(
        widget=forms.Textarea(
            attrs=styles
        ),
        initial='Lindo Ray_Ban_Original_Wayfarer')

    warranty = forms.CharField(
        widget=forms.TextInput(
            attrs=styles
        ),
        initial='60 dias'
    )

    pictures = forms.URLField(
        widget=forms.URLInput(
            attrs=styles
        ),
        initial='http://assets.ray-ban.com//is/image/RayBan/805289653653_shad_fr?$440$'
    )

    status = forms.CharField(
        widget=forms.Select(
            attrs=styles,
            choices=([
                ('active', 'Activo'),
                ('paused', 'Pausada'),
            ])))

    class Meta:
        model = Item
        fields = [
            'title',
            'category_id',
            'price',
            'currency_id',
            'available_quantity',
            'buying_mode',
            'listing_type_id',
            'condition',
            'description',
            'warranty',
            'pictures'
        ]


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
