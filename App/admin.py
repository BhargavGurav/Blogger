from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_header="B'Logger"

admin.site.register(AppUser)
admin.site.register(Blogs)
