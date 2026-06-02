from django import forms

from super_lista.items.models import ListItem, Category, ProductTemplate


class ListItemForm(forms.ModelForm):
    class Meta:
        model = ListItem
        fields = ['name', 'category', 'quantity', 'unit', 'estimated_price', 'notes', 'template']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: kg, lt, un'}),
            'estimated_price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notas opcionales'}),
            'template': forms.HiddenInput(),
        }
        labels = {
            'name': 'Producto',
            'category': 'Categoría',
            'quantity': 'Cantidad',
            'unit': 'Unidad',
            'estimated_price': 'Precio estimado ($)',
            'notes': 'Notas',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_active=True)
        self.fields['category'].required = False
        self.fields['template'].required = False
        for field in self.fields.values():
            if not isinstance(field.widget, forms.HiddenInput):
                if not hasattr(field.widget.attrs, 'class'):
                    field.widget.attrs.update({'class': 'form-control'})


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'name': 'Nombre',
            'parent': 'Categoría padre (opcional)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = Category.objects.filter(is_active=True)
        self.fields['parent'].required = False
