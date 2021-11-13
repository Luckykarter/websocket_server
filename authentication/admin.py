from django.contrib import admin
from authentication import models

class TokenAdmin(admin.ModelAdmin):
    list_display = ('owner', '__str__', 'token',)
    search_fields = ('purpose',)

admin.site.register(models.ApiToken, TokenAdmin)


class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('database_name',)
    search_fields = ('database_name',)

admin.site.register(models.SupportedDatabase, DatabaseAdmin)
