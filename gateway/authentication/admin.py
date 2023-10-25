from django.contrib import admin
from .models import * 
# Register your models here.
admin.site.register(MyAdmin)
admin.site.register( UserDetail)
admin.site.register(Address)