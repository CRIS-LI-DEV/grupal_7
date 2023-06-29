from django import forms


class LoginUsuario(forms.Form):
    usuario = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su username','class':'w3-input'}),max_length=50,required=True,label='Nombre de usuario')
    clave = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Ingrese su contraseña','class':'w3-input'}), max_length=20,label='Password',required=True,error_messages={'required':'La contraseña es obligatoria'})

class SuscripcionEmail(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Ingrese su email','class':'w3-input'}) )


class RegistroProductoForm(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del producto','class':'w3-input'}))
    precio = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Ingrese el precio','class':'w3-input'}))
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese la descripción','class':'w3-input'}))
      