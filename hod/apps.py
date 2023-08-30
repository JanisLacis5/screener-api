from django.apps import AppConfig
from .main_script import main


class HodConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hod'

    # def ready(self):
    #     main()
