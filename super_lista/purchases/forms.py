from django import forms

from super_lista.purchases.models import Purchase, PurchaseLine, Receipt


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['vendor', 'purchase_date', 'discount_total', 'tax_total', 'notes']
        widgets = {
            'vendor': forms.Select(attrs={'class': 'form-select'}),
            'purchase_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'discount_total': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'tax_total': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'vendor': 'Proveedor',
            'purchase_date': 'Fecha de compra',
            'discount_total': 'Descuento total ($)',
            'tax_total': 'Impuesto total ($)',
            'notes': 'Notas',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vendor'].required = False
        self.fields['discount_total'].required = False
        self.fields['tax_total'].required = False


class PurchaseLineForm(forms.ModelForm):
    class Meta:
        model = PurchaseLine
        fields = ['product_name', 'quantity', 'unit_price']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
        labels = {
            'product_name': 'Producto',
            'quantity': 'Cantidad',
            'unit_price': 'Precio unitario ($)',
        }


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = ['receipt_number', 'issued_at', 'file', 'notes']
        widgets = {
            'receipt_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de boleta'}),
            'issued_at': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        labels = {
            'receipt_number': 'Número de boleta',
            'issued_at': 'Emitido en',
            'file': 'Archivo',
            'notes': 'Notas',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['receipt_number'].required = False
        self.fields['issued_at'].required = False
        self.fields['file'].required = False
