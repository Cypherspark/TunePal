from django.contrib import admin
from django.apps import apps

def AUTO_REGISTER(app_name):
    app_models = apps.get_app_config(app_name).get_models()
    for model in app_models:
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass


AUTO_REGISTER('spotipy')
AUTO_REGISTER('account')
AUTO_REGISTER('music')
AUTO_REGISTER('chat')
AUTO_REGISTER('quiz')

# TokenAdmin.raw_id_fields = ['user']
# models = apps.get_models()

# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass