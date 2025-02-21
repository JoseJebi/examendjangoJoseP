from django.core.management import BaseCommand
from radioVirgen.models import Usuario, Podcast, Programa, Reproduccion, LikePrograma, LikePodcast, ListaPodcastPendientes, MetodoPago, UsuariosPago

class Command(BaseCommand):
    help = 'Carga de 3 metodos de pago para el usuario 1'

    def handle(self, *args, **kwargs):
        metodo1 = MetodoPago.objects.create(tipo="Tarjeta", numTarjeta="12345", cvc="123", nombreTitular="Jaime Alemany")   #acaba de entrar por la puerta conforme escribo esto
        metodo2 = MetodoPago.objects.create(tipo="PayPal", email="cifpvirgen@educamosclm.es")
        metodo3 = MetodoPago.objects.create(tipo="Transferencia", numCuenta="12345", nombreTitular="Jaime Alemany")
        metodo4 = MetodoPago.objects.create(tipo="Bizum", tlf="+341312")

        pagoUsuario1 = UsuariosPago.objects.create(usuario=Usuario.objects.get(id=1), metodo=metodo1)
        pagoUsuario2 = UsuariosPago.objects.create(usuario=Usuario.objects.get(id=1), metodo=metodo2, pref=True)
        pagoUsuario3 = UsuariosPago.objects.create(usuario=Usuario.objects.get(id=1), metodo=metodo3)
        pagoUsuario4 = UsuariosPago.objects.create(usuario=Usuario.objects.get(id=1), metodo=metodo4)