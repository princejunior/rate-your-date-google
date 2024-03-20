from django.apps import AppConfig


class RmdWebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rmd_web'

    def ready(self):
        import rmd_web.signals  # This imports the signals file when Django starts