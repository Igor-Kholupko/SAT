from django.contrib import admin
from django.contrib.auth.models import Group

from custom_auth.models import User, Group as CustomGroup

admin.site.unregister(Group)

admin.site.register(User)
admin.site.register(CustomGroup)
