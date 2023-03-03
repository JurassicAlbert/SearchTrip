from .models.user import User
from django.contrib import admin
from .models.review import Review
from .models.address import Address
from .models.location import Location
from .models.response import Response
from .models.favorite import Favorite

admin.site.register(User)
admin.site.register(Address)
admin.site.register(Location)
admin.site.register(Review)
admin.site.register(Response)
admin.site.register(Favorite)
