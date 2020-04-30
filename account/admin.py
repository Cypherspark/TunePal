from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin
from django.apps import apps


TokenAdmin.raw_id_fields = ['user']
models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass