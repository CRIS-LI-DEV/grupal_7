"""
URL configuration for proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1.views import  *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    
    path('admin/', admin.site.urls),
    
    path('',HomeRegister.as_view(), name='home'),

    path('login_view/', Login_View.as_view(),name='login_view'),
    path('perfil/', login_required(perfil_cliente),name='perfil'),
    path('perfil/', login_required(perfil_empleado),name='perfil'),
    path('logout_view/', logout_view,name='logout_view'),
    path('lista/', listar_pedidos,name='lista'),
    path('pedido/<int:id>', visualizar_pedidos, name='lista'),
    path('registro_producto/', RegistroProducto.as_view(),name='registro_producto'),
    path('productos/', lista_producto,name='lista'),
    path('producto/<int:id_pr>', visualizacion_producto,name='lista'),
    
    path('tomar_pedido_staff/', TomarPedidoStaff.as_view(),name='asdasdsa'),
    path('x/', funcion_para_guardar,name='asdasdsa'),
    path('finalizar_pedido_staff',FinalizarPedidoStaff.as_view(),name='FINALIZAR_PEDIDO'),
     path('finalizar_pedido_cliente/',FinalizarPedidoCliente.as_view(),name='FINALIZAR_PEDIDO'),
     path('limpiar_carrito/', limpiar_carrito,name="LIMPIAR_CARRITO")
   
]
