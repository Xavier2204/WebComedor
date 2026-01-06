from django import forms
from .models import Transaccion

class TransaccionForm(forms.ModelForm): # Clase corregida
    class Meta:
        model = Transaccion
        fields = ['tipo', 'categoria', 'monto', 'descripcion']
        widgets = {
            'tipo': forms.HiddenInput(),
            'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pago de luz'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }