# api/admin.py

#from django.contrib import admin
#from .models.user import User
#from .models.shelter_user import shelter_user

#@admin.register(User)
#class UserAdmin(admin.ModelAdmin):
#   list_display = ('email', 'nombre', 'telefono', 'is_staff', 'is_active')
#    search_fields = ('email', 'nombre')

#@admin.register(ShelterUser)
#class ShelterUserAdmin(admin.ModelAdmin):
#    list_display = ('email', 'nombre', 'telefono', 'estado', 'ciudad', 'direccion', 'codigoPostal')
#    search_fields = ('email', 'nombre')

from django.contrib import admin
from .models.user import User
from .models.shelter_user import ShelterUser

admin.site.register(User)
admin.site.register(ShelterUser)