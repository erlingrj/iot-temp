from django.contrib import admin
from .models import Question

# Tell admin that Question objects should have
# admin interface
admin.site.register(Question)