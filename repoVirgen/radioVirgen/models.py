from django.db import models

class Programa(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    descripcion = models.CharField(max_length=300)
    fecha_alta = models.DateField(null=True,blank=True)
    fecha_baja = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Programa manage{self.nombre}'

class Podcast(models.Model):
    nombre = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=300)
    categoria = models.CharField(max_length=50)
    fecha_alta = models.DateField(null=True, blank=True)
    fecha_baja = models.DateField(null=True, blank=True)
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, related_name="podcast")
    link_drive = models.CharField(max_length=255)

    def __str__(self):
        return f'Podcast {self.nombre}'

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(categoria__in=["Educativo", "Comedia", "Formación"]),
                name="check_categoria_values"
            )
        ]

class Autor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=125)
    fecha_nac = models.DateField(null=True, blank=True)
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, related_name="autores")

    def __str__(self):
        return f'Autor: {self.nombre} {self.apellido}'

class AutorPodcast(models.Model):
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="podcastAutores")
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name="autoresPodcast")

    def __str__(self):
        return f'Autor {self.autor} hace podcast {self.podcast}'


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nick = models.CharField(max_length=100, unique=True)
    fecha_nac = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Nombre: {self.nombre}\n Nick: {self.nick}'

class Reproduccion(models.Model):
    usuario= models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuarioReproduccion')
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='podcastReproduccion')

    def __str__(self):
        return f'Podcast ${self.podcast} reproducido por {self.usuario}'

class ListaPodcastPendientes(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuarioPendientes')
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='podcastPendientes')

    def __str__(self):
        return f'Usuario {self.usuario}, podcast {self.podcast}'

class LikePrograma(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuarioLikePro')
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, related_name='programaLike')

    def __str__(self):
        return f'Usuario {self.usuario} programa {self.programa}'


class LikePodcast(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuarioLikePod')
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='podcastLike')

    def __str__(self):
        return f'Usuario {self.usuario} podcast {self.podcast}'

class MetodoPago(models.Model):
    tipo = models.CharField(max_length=80)
    numTarjeta = models.CharField(max_length=20,null=True,blank=True, default=None)
    cvc = models.CharField(max_length=3, null=True, blank=True, default=None)
    nombreTitular = models.CharField(max_length=80, null=True, blank=True, default=None)
    email = models.CharField(max_length=50, null=True, blank=True, default=None)
    numCuenta = models.CharField(max_length=30, null=True, blank=True, default=None)
    tlf = models.CharField(max_length=20, null=True, blank=True, default=None)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(tipo__in=["Tarjeta", "PayPal", "Transferencia", "Bizum"]), #Si, soy un chulito y he puesto Bizum también
                name="check_tipo_pago_values"
            )
        ]

    def __str__(self):
        return f'tipo {self.tipo}'

class UsuariosPago(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuarioMetPago')
    metodo = models.ForeignKey(MetodoPago, on_delete=models.CASCADE, related_name='metodoUsuario')
    pref = models.BooleanField(default=False)

    def __str__(self):
        salida = f'Usuario {self.usuario}, metodo {self.metodo}'
        if self.pref:
            salida+=f' pref: Si'
        else:
            salida += f' pref: No'

        return salida