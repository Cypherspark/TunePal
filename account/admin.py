from django.contrib import admin
from django.conf import settings


settings.auto_register_models('spotipy')
settings.auto_register_models('account')
settings.auto_register_models('music')
settings.auto_register_models('chat')
settings.auto_register_models('quiz')

# TokenAdmin.raw_id_fields = ['user']
# models = apps.get_models()

# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass