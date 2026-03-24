from django import forms
from Administracion.models import Cliente, Cuenta, Transaccion


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['nombre', 'dpi', 'telefono']


class CuentaForm(forms.ModelForm):

    class Meta:
        model = Cuenta
        fields = ['cliente', 'numero_cuenta', 'tipo_cuenta', 'saldo']


class TransaccionForm(forms.ModelForm):

    class Meta:
        model = Transaccion
        fields = ['cuenta', 'tipo', 'monto', 'descripcion']

class TransferenciaForm(forms.Form):
    de_cuenta = forms.CharField()
    a_cuenta = forms.CharField()
    monto = forms.IntegerField()
    descripcion = forms.CharField()
    
class FiltrarForm(forms.Form):
    
    fecha = forms.DateTimeField()
    