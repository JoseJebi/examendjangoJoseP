from django.core.management import BaseCommand
from django.db.utils import DatabaseError, OperationalError
from radioVirgen.models import Usuario, Podcast, Programa, Reproduccion, LikePrograma, LikePodcast, ListaPodcastPendientes, MetodoPago, UsuariosPago

class Command(BaseCommand):
    help = 'Listar métodos de pago de un usuario por su ID'

    def add_arguments(self, parser):
        parser.add_argument(
            '--uid',
            type=int,
            help='ID del usuario',
            required=True
        )

    def handle(self, *args, **kwargs):
        try:
            usuario_id = kwargs['uid']

            try:
                metodos = UsuariosPago.objects.filter(usuario=Usuario.objects.get(id=usuario_id))
            except UsuariosPago.DoesNotExist:
                self.stderr.write("Este usuario no tiene métodos de pago.")
                return
            except Usuario.DoesNotExist:
                self.stderr.write("Error: No se encontró el usuario con ese ID.")
                return

            for metodo in metodos:
                self.stdout.write(f"- {metodo}")

        except (DatabaseError, OperationalError) as db_error:
            self.stderr.write(f"Error en la base de datos: {db_error}")
        except Exception as e:
            self.stderr.write(f"Error inesperado: {e}")