from django.contrib import admin
from .models import Profile
from .models import Category
from .models import List

# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(List)

