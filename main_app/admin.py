from django.contrib import admin
from django.contrib.auth.models import User, Group

from main_app.models import Document

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(Document)
