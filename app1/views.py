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
        request.session['carrito']=[{"producto":1,"cantidad":3}] 
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
            comuna= Comuna.objects.get(id=4)
            region= Region.objects.get(id=4)
            perfil_cliente=Cliente(user = usuario,
            telefono='',
            direccion='',
            rut='',
            comuna = comuna,
            region = region,
            correo=email


            )
            perfil_cliente.save()
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
                
                print(usuario_busqueda.username)
                print(password)
                user = authenticate(request, username=usuario_busqueda.username, password=password)
                print(user)
                if user is not None:
                    if user.is_active:
                        login(request,user)
                        cliente = Cliente.objects.filter(
                        user_id=user.id).count()
                        empleado = Empleado.objects.filter(
                        user_id=user.id).count()
                        if cliente ==1 and empleado == 0 :
                            return redirect('/perfil_cliente/')
                        if cliente ==0 and empleado == 1 :
                            return redirect('/perfil_empleado/')







                        # return redirect('/perfil/')
                    else:
                        return HttpResponse("NO FUNCIONO")
                else:
                    return HttpResponse("NO FUNCIONO")
        



def perfil_cliente(request):
    cliente = Cliente.objects.get(user_id=request.user.id)
    carritos=Carrito.objects.filter(cliente_id = cliente.id)
    pedidos = []
    print(carritos)
    for x in carritos:
        pedido = Pedido.objects.get(carrito_id=x.id)
        pedidos.append(pedido)
        print(pedido.id)
    print(pedidos)
    context ={ 'carritos':pedidos }
    
    return render(request, 'perfil_cliente.html',context)

def perfil_empleado(request):
    pedidos = Pedido.objects.all()
    context={'lista':pedidos}
    return render(request, 'perfil_empleado.html',context)

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


    

def visualizar_pedidos_e(request,id):
    template="pedido_estado.html"
    pedido = Pedido.objects.get(id=id)
    carrito = Carrito.objects.get(id=pedido.carrito_id)
    detalles = DetalleProductoSocilicitado.objects.filter(carrito_id = carrito.id)
    suma_precio=0
    for x in detalles:
        suma_precio = suma_precio + (x.producto.precio * x.cantidad)
        

    suma_cantidad= DetalleProductoSocilicitado.objects.filter(carrito_id = carrito.id).aggregate(total=Sum('cantidad'))
   
    formulario_estado = FormularioEstado()
    context={'pedido':pedido,
             'carrito':carrito,
             'detalles':detalles,
             'suma_precio':suma_precio,
             'suma_cantidad':suma_cantidad['total'] ,
             'formulario':formulario_estado    
             }
    return render(request,template,context)






def visualizacion_producto(request, id_pr):
    template="producto.html"
    producto = Producto.objects.get(id=id_pr)
    context={'producto': producto}
    return HttpResponse(context['producto'])
    #return render(request,template,context)


class TomarPedidoStaff(View):
   
    id_carrito = None
    def get(self,request):
   
        carrito = Carrito(precio_total=0,cantidad_total=0)
        carrito.save()
        self.id_carrito = carrito.id
       
        lista = Producto.objects.all()
        carrito = request.session.get("carrito")     
        template="tomar_pedido_staff.html"
       
        return render(request,template,context={'lista':lista, 'carrito': carrito})
        #return HttpResponse(lista)
    def post(self,request):
        pass


class TomarPedidoCliente(View):
   
    id_carrito = None
    def get(self,request):
   
        carrito = Carrito(precio_total=0,cantidad_total=0)
        carrito.save()
        self.id_carrito = carrito.id
       
        lista = Producto.objects.all()
        carrito = request.session.get("carrito")     
        template="tomar_pedido_cliente.html"
       
        return render(request,template,context={'lista':lista, 'carrito': carrito})
        #return HttpResponse(lista)
    def post(self,request):
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

def funcion_para_guardar_cliente(request):
    if request.method=="POST":
        formulario = AgregarProductoFrom(request.POST)

        if request.session.get('carrito') == None:
        
            request.session['carrito']=[]
        
        carrito = request.session.get('carrito')
        producto = Producto.objects.get(id=formulario['producto_id'].value())
        carrito.append({"producto":formulario['producto_id'].value(),"cantidad":formulario['cantidad_id'].value(),'nombre':producto.nombre})
        
        request.session['carrito'] = carrito
        return redirect('/tomar_pedido_cliente/')



def funcion_para_guardar_staff(request):
    if request.method=="POST":
        formulario = AgregarProductoFrom(request.POST)

        if request.session.get('carrito') == None:
        
            request.session['carrito']=[]
        
        carrito = request.session.get('carrito')
        
        producto = Producto.objects.get(id=formulario['producto_id'].value())

        carrito.append({"producto":formulario['producto_id'].value(),"cantidad":formulario['cantidad_id'].value(),'nombre':producto.nombre})
        
        request.session['carrito'] = carrito
        return redirect('/tomar_pedido_staff/')

class FinalizarPedidoStaff(View):
    def get(self,request):
        print("STAFF")
        carrito = request.session.get('carrito')
        print("STAFF2")
        formulario = FormularioPedidoStaff()
        template = 'finalizar_pedido_staff.html'
        context = {'formulario':formulario,'carrito':carrito}
        
        return render(request,template,context)
        
        

    def post(self,request):
        formulario = FormularioPedidoStaff(request.POST)
   
        if formulario.is_valid():
            email = formulario.cleaned_data['cliente_email']
            usuario_cliente =  User.objects.get(email=email)
            print(usuario_cliente)
            cliente = Cliente.objects.get(user_id= usuario_cliente.id)
            usuario_empleado =  User.objects.get(id=request.user.id)
           
            empleado = Empleado.objects.get(user_id=request.user.id)
            
            carrito= Carrito(
                cantidad_total= 0,
                precio_total=0,
                cliente = cliente,
                empleado = empleado 
                 )
            carrito.save()
            carrito_session = request.session.get('carrito')
            suma_precio=0
            for x in carrito_session:
                producto = Producto.objects.get(id=x['producto'])
                cantidad = x['cantidad']
                detalle = DetalleProductoSocilicitado(
                    producto =producto,
                    cantidad= cantidad,
                    valor_producto = producto.precio,
                    carrito = carrito
                 )
                detalle.save()
                suma_precio = suma_precio + (int(producto.precio) *int(cantidad))
            suma_cantidad= DetalleProductoSocilicitado.objects.filter(carrito_id = carrito.id).aggregate(total=Sum('cantidad'))

           
            carrito.cantidad_total = suma_cantidad['total']
            carrito.precio_total = suma_precio
            carrito.save()

            estado = EstadoPedido.objects.get(id=1)
            comuna = Comuna.objects.get(nombre=formulario.cleaned_data['comuna'])
            region = Region.objects.get(nombre=formulario.cleaned_data['region'])
            pedido = Pedido( 
                    fecha = formulario.cleaned_data['fecha_entrega'],
                    estado=estado,
                    calle_entrega=formulario.cleaned_data['direccion'],
                    comuna=comuna,
                    region=region,
                    carrito = carrito         
                    
                )        

            pedido.save()
            return redirect('/perfil_empleado')


class FinalizarPedidoCliente(View):
    def get(self,request):
        carrito = request.session.get('carrito')
        formulario = FormularioPedidoCliente()
        template = 'finalizar_pedido_cliente.html'
        context = {'formulario':formulario,'carrito':carrito}
        return render(request,template,context)
        

    def post(self,request):
        formulario = FormularioPedidoCliente(request.POST)
       
        if formulario.is_valid():
          
            usuario_cliente =  User.objects.get(email=request.user.email)

            cliente = Cliente.objects.get(user_id= usuario_cliente.id)
        
            
            carrito= Carrito(
                cantidad_total= 0,
                precio_total=0,
                cliente = cliente
      
                 )
            carrito.save()
            carrito_session = request.session.get('carrito')
            suma_precio=0
            for x in carrito_session:
                producto = Producto.objects.get(id=x['producto'])
                cantidad = x['cantidad']
                detalle = DetalleProductoSocilicitado(
                    producto =producto,
                    cantidad= cantidad,
                    valor_producto = producto.precio,
                    carrito = carrito
                 )
                detalle.save()
                suma_precio = suma_precio + (int(producto.precio) * int(cantidad))
            suma_cantidad= DetalleProductoSocilicitado.objects.filter(carrito_id = carrito.id).aggregate(total=Sum('cantidad'))
            carrito.cantidad_total = suma_cantidad['total']
            carrito.precio_total = suma_precio
            carrito.save()
            estado = EstadoPedido.objects.get(id=1)
            comuna = Comuna.objects.get(nombre=formulario.cleaned_data['comuna'])
            region = Region.objects.get(nombre=formulario.cleaned_data['region'])
            pedido = Pedido( 
                    fecha = formulario.cleaned_data['fecha_entrega'],
                    estado=estado,
                    calle_entrega=formulario.cleaned_data['direccion'],
                    comuna=comuna,
                    region=region,
                    carrito = carrito         
                    
                )        

            pedido.save()
            return redirect('/perfil_cliente')


def limpiar_carrito_staff(request):
    request.session['carrito']=[]
    return redirect('/tomar_pedido_staff/')

def limpiar_carrito_cliente(request):
    request.session['carrito']=[]
    return redirect('/tomar_pedido_cliente/')



def modificar_estado_pedido(request,id_pedido):
    
    formulario = FormularioEstado(request.POST)

    if formulario.is_valid():
        nombre_estado = formulario.cleaned_data['estado']
        estado = EstadoPedido.objects.get(nombre=nombre_estado)
        pedido=Pedido.objects.get(id=id_pedido)
        pedido.estado = estado
        pedido.save()
        
        email = pedido.carrito.cliente.user.email
        print(email)
        destinatarios=[email]
        asunto = 'ESTADO DE TU PEDIDO'
        cuerpo = 'TU PEDIDO ESTA ' + nombre_estado
               
        send_mail(
            asunto,
            cuerpo,
            'talento@fabricadecodigo.dev',
            destinatarios,
            fail_silently=False,
        )
        direccion='/pedido_e/'+ str(id_pedido)
        return redirect(direccion)




