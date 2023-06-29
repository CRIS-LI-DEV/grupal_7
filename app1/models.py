
from django.db import models
from django.contrib.auth.models import User

# ENTIDADES 
class Comuna(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre}"

class Region(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre}"

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=100)
    correo = models.CharField(max_length=200,unique=True)
    direccion = models.CharField(max_length=100)
    comuna= models.ForeignKey(Comuna, on_delete=models.CASCADE)
    region= models.ForeignKey(Region, on_delete=models.CASCADE)
    rut= models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}|{self.user.last_name}|{self.comuna}"


class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=100)
    correo = models.CharField(max_length=200,unique=True)
    direccion = models.CharField(max_length=100)
    comuna= models.ForeignKey(Comuna, on_delete=models.CASCADE)
    region= models.ForeignKey(Region, on_delete=models.CASCADE)
    rut= models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}|{self.user.first_name}|{self.user.last_name}|{self.comuna}"



class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    descripcion= models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre}|{self.precio}|{self.descripcion}"



class Carrito(models.Model):
    cantidad_total =   models.IntegerField( null=True)
    precio_total = models.IntegerField( null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, null=True)# NULL o ID EMPLEADO, if x== NULL
    
    def __str__(self):
        return f"{self.cantidad_total}|{self.precio_total}|{self.cliente.user.username}|{self.cliente.user.username}"

class DetalleProductoSocilicitado(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    valor_producto = models.IntegerField()
    cantidad = models.IntegerField()

    
    def __str__(self):
        return f"{self.producto.nombre}|{self.carrito}|{self.cantidad}"


class EstadoPedido(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.nombre}"

class Pedido(models.Model):
    fecha = models.DateField()
    estado = models.ForeignKey(EstadoPedido, on_delete=models.CASCADE)
    calle_entrega = models.CharField(max_length=200)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    carrito = models.ForeignKey(Carrito , on_delete=models.CASCADE)
    region= models.ForeignKey(Region, on_delete=models.CASCADE)

    
    def __str__(self):
        return f"{self.fecha}|{self.estado}|{self.calle_entrega}|{self.comuna}"




