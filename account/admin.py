from django.contrib import admin
from django.conf import settings


settings.AUTO_REGISTER('spotipy')
settings.AUTO_REGISTER('account')
settings.AUTO_REGISTER('music')
settings.AUTO_REGISTER('chat')
settings.AUTO_REGISTER('quiz')

# TokenAdmin.raw_id_fields = ['user']
# models = apps.get_models()

# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass