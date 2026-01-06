from django import forms
from .models import Beneficiary, Representative, Enrollment

class RepresentativeForm(forms.ModelForm):
    class Meta:
        model = Representative
        fields = ['nombre', 'ci', 'nacionalidad', 'empleo', 'ingresos', 'convivencia']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ci': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidad': forms.TextInput(attrs={'class': 'form-control'}),
            'empleo': forms.TextInput(attrs={'class': 'form-control'}),
            'ingresos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'convivencia': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        # Usamos los nombres exactos de tu modelo: representative, nacimiento, ci...
        fields = ['representative', 'nombre', 'apellidos', 'ci', 'nacimiento', 
                'nacionalidad', 'direccion', 'contacto', 'monthly_fee', 'active']
        widgets = {
            'representative': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'ci': forms.TextInput(attrs={'class': 'form-control'}),
            'nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nacionalidad': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'monthly_fee': forms.NumberInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['escuela', 'grado']
        widgets = {
            'escuela': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la escuela'}),
            'grado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 5to Grado'}),
        }