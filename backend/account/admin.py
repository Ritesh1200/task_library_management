from pyexpat import model
from django.contrib import admin

from account import models

admin.site.register(models.User)