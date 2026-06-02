from django import forms

from super_lista.lists.models import ShoppingList, Invitation, ListMember


class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['name', 'description', 'frequency_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Lista del mes'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción opcional'}),
            'frequency_type': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'frequency_type': 'Frecuencia',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not hasattr(field.widget.attrs, 'class'):
                field.widget.attrs.update({'class': 'form-control'})


class ShareListForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.cl'}),
        label='Correo electrónico del invitado',
    )
    role = forms.ChoiceField(
        choices=Invitation.RoleChoices.choices,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Rol',
    )


class InvitationAcceptForm(forms.Form):
    """Just a confirm form, no fields needed beyond CSRF token."""
    pass
