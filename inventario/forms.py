# inventario/forms.py
from django import forms
from .models import Producto, MovimientoInventario

class ProductoForm(forms.ModelForm):
    CATEGORIAS = [('verduras', 'Verduras'), ('frutas', 'Frutas'), ('carbohidratos', 'Carbohidratos'), ('granos', 'Granos'), ('proteinas', 'Proteinas'),('varios', 'Varios')]
    UNIDADES = [('lb', 'Libras (lb)'), ('kg', 'Kilogramos (kg)'), ('un', 'Unidades'), ('lt', 'Litros')]

    categoria = forms.ChoiceField(choices=CATEGORIAS, widget=forms.Select(attrs={'class': 'form-select'}))
    unidad_medida = forms.ChoiceField(choices=UNIDADES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'unidad_medida', 'cantidad_actual', 'cantidad_minima']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad_actual': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_minima': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = MovimientoInventario
        fields = ['producto', 'tipo', 'cantidad', 'comentario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'comentario': forms.TextInput(attrs={'class': 'form-control'}),
        }