from django.contrib import admin

from .models import *


admin.site.register(Category)
admin.site.register(Pin)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(Profile)
