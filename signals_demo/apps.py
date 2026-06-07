from django.apps import AppConfig


class SignalsDemoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'signals_demo'

    def ready(self):
        # Importing signals here ensures they are registered
        # when Django starts up — the standard Django way.
        import signals_demo.signals  # noqa
