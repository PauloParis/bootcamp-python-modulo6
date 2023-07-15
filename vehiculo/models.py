from django.db import models, migrations



# Create your models here.

class VehiculosModel(models.Model):

    marca_choices = (
        ('Fiat', 'Fiat'),
        ('Chevrolet', 'Chevrolet'),
        ('Ford', 'Ford'),
        ('Toyota', 'Toyota')
    )
    marca = models.CharField(max_length=20, default='Ford', choices=marca_choices)
    modelo = models.CharField(max_length=100)
    serial_carroceria = models.CharField(max_length=50)
    serial_motor = models.CharField(max_length=50)
    # Particular, transporte y carga.
    categoria_choices = (
        ('Particular', 'Particular'),
        ('Transporte', 'Transporte'),
        ('Carga', 'Carga')
    )
    categoria = models.CharField(max_length=20, default='Particular', choices=categoria_choices)
    precio = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)


    class Meta:
        permissions = (
            ('visualizar_catalogo', 'Puede visualizar catálogo'),
        )


    def __str__(self) -> str:
        return f'''
            Vehiculo:
                marca: {self.marca}
                modelo: {self.modelo} 
                serial_carroceria: {self.serial_carroceria} 
                serial_motor: {self.serial_motor} 
                categoria: {self.categoria} 
                precio: {self.precio}
                creación: {self.fecha_creacion} 
                modificado: {self.fecha_modificacion} 
        '''
    
