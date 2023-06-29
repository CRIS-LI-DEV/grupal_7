from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from app1.forms import *
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
import string
import random
from django.core.mail import send_mail
import uuid
from app1.models import *

from django.db.models import Sum

def generar_usuario_aleatorio():
    usuario_aleatorio = "usuario" + str(uuid.uuid4())
    return str(usuario_aleatorio)

class HomeRegister(View):
    def get(self,request):
        formulario = SuscripcionEmail()
        context = {"formulario":formulario}
        return render (request, 'home.html', context)
    def post(self,request):

        formulario = SuscripcionEmail(request.POST)
        email_formulario = formulario['email'].value()
   
        cantidad_usuarios = User.objects.filter(email=email_formulario).count()

        if cantidad_usuarios > 0:
                 return HttpResponse("EMAIL EXISTENTE")


        # emails_usuarios =  User.objects.values_list('email', flat=True)
        # for email in emails_usuarios:
        #     print(email)




        if formulario.is_valid():
            nombre_usuario = generar_usuario_aleatorio()
            clave = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            email = formulario.cleaned_data['email']
           
            usuario = User( email = email, username = nombre_usuario)
            usuario.password = make_password(clave)
            usuario.save()

            asunto = 'CONFIRMACION SUSCRIPCION'
            cuerpo = 'USERNAME : '+ nombre_usuario+ '\nCORREO : '+ email + '\nTU CLAVE ES : ' + clave
            print(formulario['email'])
            destinatarios=[email]
            
            send_mail(
            asunto,
            cuerpo,
            'talento@fabricadecodigo.dev',
            destinatarios,
            fail_silently=False,
        )


            return redirect('/login_view/')



class Login_View(View):
    template_name = 'login.html'

    def get(self,request):
        formulario = LoginUsuario()
        context={'formulario': formulario}
        #return HttpResponse('prueba')
        return render(request,self.template_name,context)
    
    def post(self,request):
            formulario =  LoginUsuario(request.POST)           
            if formulario.is_valid():
                usuario= formulario.cleaned_data['usuario']
                password = formulario.cleaned_data['clave']
                
                usuario_busqueda = User.objects.get(email=usuario)
                
                print(usuario)
                print(password)
                user = authenticate(request, username=usuario_busqueda.username, password=password)
                print(user)
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        return redirect('/perfil/')
                    else:
                        return HttpResponse("NO FUNCIONO")
                else:
                    return HttpResponse("NO FUNCIONO")
        



def perfil(request):
    return render(request, 'perfil.html')

def logout_view(request):

    print('logout')
    logout(request)
    return redirect('/')


def listar_pedidos(request):
    template="lista_pedidos.html"
    pedidos = Pedido.objects.all()
    context={'lista':pedidos}
   
    return render(request,template,context)


def visualizar_pedidos(request,id):
    template="pedido.html"
    pedido = Pedido.objects.get(id=id)
    carrito = Carrito.objects.get(id=pedido.carrito_id)
    detalles = DetalleProductoSocilicitado.objects.filter(carrito_id = carrito.id)
    suma_precio=0
    for x in detalles:
        suma_precio = suma_precio + (x.producto.precio * x.cantidad)
        

    suma_cantidad= DetalleProductoSocilicitado.objects.filter(carrito_id = carrito.id).aggregate(total=Sum('cantidad'))
   
  
    context={'pedido':pedido,
              'carrito':carrito,
              'detalles':detalles,
                'suma_precio':suma_precio,
                'suma_cantidad':suma_cantidad['total'] 
             }
    return render(request,template,context)




class TomarPedidoStaff(View):
    def get(request,self):
        template=""
        return render(request,template,context={})
    def post(request,self):
        pass

    

class RegistroProducto(View):
        def get(self, request):
            template='registro_producto.html'
            context = {'formulario': RegistroProductoForm}
            return render(request,template,context)
        
        def post(self, request):
            formulario = RegistroProductoForm(request.POST)
            if formulario.is_valid():
                producto = Producto(nombre =formulario['nombre'].value(),  precio =formulario['precio'].value(), descripcion = formulario['descripcion'].value() )
                producto.save()
                return redirect("/productos/")

def lista_producto(request):
          template= 'lista_productos.html'
          context={'lista': Producto.objects.all()}
          return render(request,template,context)