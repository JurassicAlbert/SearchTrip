from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Location)
admin.site.register(Review)
admin.site.register(Response)
admin.site.register(Favorite)

