from django import forms
from app1.models import *


class LoginUsuario(forms.Form):
    usuario = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su username','class':'w3-input'}),max_length=50,required=True,label='Nombre de usuario')
    clave = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña','class':'w3-input'}), max_length=20,label='Password',required=True,error_messages={'required':'La contraseña es obligatoria'})

class SuscripcionEmail(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Ingrese su email','class':'w3-input'}) )


class RegistroProductoForm(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del producto','class':'w3-input'}))
    precio = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Ingrese el precio','class':'w3-input'}))
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese la descripción','class':'w3-input'}))
      

class AgregarProductoFrom(forms.Form):
       producto_id = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Ingrese el precio','class':'w3-input'}))
       cantidad_id = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Ingrese el precio','class':'w3-input'}))

class FormularioPedidoStaff(forms.Form):

        opciones_region = Region.objects.all().values_list('nombre', flat=True)
        opciones_comuna = Comuna.objects.all().values_list('nombre', flat=True)
    
        OPCIONES_REGION = tuple([(opcion, opcion) for opcion in opciones_region])
        OPCIONES_COMUNA = tuple([(opcion, opcion) for opcion in opciones_comuna] )
        
    

        direccion=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese la direccion del pedido','class':'w3-input'}))
        fecha_entrega = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class':'w3-input'}))
        cliente_email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Ingrese el email para identificar el cliente','class':'w3-input'}))
        
        

        region = forms.ChoiceField(
        choices=OPCIONES_REGION,
        widget=forms.Select(attrs={'class':'w3-input'}))

        comuna = forms.ChoiceField(
        choices=OPCIONES_COMUNA,
        widget=forms.Select( attrs={'class':'w3-input'}))


class FormularioPedidoCliente(forms.Form):

        opciones_region = Region.objects.all().values_list('nombre', flat=True)
        opciones_comuna = Comuna.objects.all().values_list('nombre', flat=True)
    
        OPCIONES_REGION = tuple([(opcion, opcion) for opcion in opciones_region])
        OPCIONES_COMUNA = tuple([(opcion, opcion) for opcion in opciones_comuna] )
        
    

        direccion=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese la direccion del pedido','class':'w3-input'}))
        fecha_entrega = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class':'w3-input'}))
        
        

        region = forms.ChoiceField(
        choices=OPCIONES_REGION,
        widget=forms.Select(attrs={'class':'w3-input'}))

        comuna = forms.ChoiceField(
        choices=OPCIONES_COMUNA,
        widget=forms.Select( attrs={'class':'w3-input'}))




class FormularioEstado(forms.Form):

        opciones_estado = EstadoPedido.objects.all().values_list('nombre', flat=True)
    
        OPCIONES_ESTADO = tuple([(opcion, opcion) for opcion in opciones_estado] )
        
        estado = forms.ChoiceField(
        choices=OPCIONES_ESTADO,
        widget=forms.Select( attrs={'class':'w3-input'}))