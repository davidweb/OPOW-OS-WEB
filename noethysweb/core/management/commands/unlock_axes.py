from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import transaction

class Command(BaseCommand):
    help = "Débloquer les blocs créés par django-axes. Utiliser --username, --ip ou --all."

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username', help="Nom d'utilisateur à débloquer")
        parser.add_argument('-i', '--ip', help="Adresse IP à débloquer")
        parser.add_argument('--all', action='store_true', help="Supprimer tous les enregistrements axes")

    def handle(self, *args, **options):
        username = options.get('username')
        ip = options.get('ip')
        delete_all = options.get('all')

        try:
            app_config = apps.get_app_config('axes')
        except LookupError:
            self.stdout.write(self.style.ERROR('L\'application "axes" n\'est pas installée dans ce projet.'))
            return

        total_deleted = 0
        models = list(app_config.get_models())

        if not models:
            self.stdout.write(self.style.WARNING('Aucun modèle trouvé dans l\'app "axes".'))
            return

        def find_field(model, candidates):
            fields = {f.name for f in model._meta.get_fields()}
            for c in candidates:
                if c in fields:
                    return c
            return None

        username_fields = ('username', 'user', 'attempt_username', 'username_attempt')
        ip_fields = ('ip_address', 'ip', 'ipaddr')

        with transaction.atomic():
            for model in models:
                qs = model.objects.all()
                # Appliquer filtres si nécessaire
                if not delete_all:
                    filtered = False
                    if username:
                        f = find_field(model, username_fields)
                        if f:
                            qs = qs.filter(**{f: username})
                            filtered = True
                    if ip:
                        f = find_field(model, ip_fields)
                        if f:
                            qs = qs.filter(**{f: ip})
                            filtered = True
                    # Si ni username ni ip trouvés dans ce modèle, ignorer (évite suppressions non voulues)
                    if (username or ip) and not filtered:
                        continue

                count = qs.count()
                if count:
                    qs.delete()
                    total_deleted += count
                    self.stdout.write(self.style.SUCCESS(
                        f'Supprimé {count} enregistrement(s) dans {model._meta.label}'
                    ))

        if total_deleted == 0:
            if delete_all:
                self.stdout.write(self.style.WARNING('Aucun enregistrement axes trouvé à supprimer.'))
            else:
                self.stdout.write(self.style.WARNING('Aucun enregistrement correspondant trouvé (username/ip).'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Total supprimé : {total_deleted} enregistrement(s)'))
