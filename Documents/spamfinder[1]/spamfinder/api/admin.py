from django.contrib import admin
from .models import ClientUser, Contact, PhoneNumber

admin.site.register(ClientUser)
admin.site.register(Contact)
admin.site.register(PhoneNumber)